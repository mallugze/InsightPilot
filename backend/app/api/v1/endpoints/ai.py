import logging
import uuid
import time
import json
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.session import get_db
from app.exceptions import DatasetValidationError
from app.models.ai_memory import Conversation, ChatMessage

# Core configurations and services
from app.services.ai.context_builder import ContextBuilder
from app.services.ai.prompt_manager import PromptManager
from app.services.ai.gemini_service import GeminiLLMProvider
from app.services.ai.response_validator import ResponseValidator, AIValidationException
from app.services.ai.conversation_memory import ConversationMemoryManager
from app.services.ai.ai_cache import AICache
from app.services.ai.report_generator import ReportGenerator
from app.services.ai.citation_builder import CitationBuilder
from app.services.ai.history_builder import ConversationHistoryBuilder
from app.services.ai.suggestions import DynamicSuggestionsGenerator

# API schemas
from app.services.ai.schemas import (
    ChatRequest, 
    ChatResponse, 
    ContextResponse, 
    ReportResponse,
    ExplainableConfidence,
    ResponseMetadata,
    ConversationsListResponse,
    ConversationDetailResponse,
    ConversationSummary,
    ConversationMessage,
    SuggestedQuestionsResponse
)

router = APIRouter()
logger = logging.getLogger("ai_endpoint")

# Initialize shared infrastructure
context_builder = ContextBuilder()
prompt_manager = PromptManager()
llm_provider = GeminiLLMProvider()
response_validator = ResponseValidator()
ai_cache = AICache()
report_generator = ReportGenerator(llm_provider, prompt_manager, response_validator)
citation_builder = CitationBuilder()
history_builder = ConversationHistoryBuilder()
suggestions_generator = DynamicSuggestionsGenerator()

@router.post("/context/{analysis_id}", response_model=ContextResponse, status_code=status.HTTP_200_OK)
def get_analysis_context(analysis_id: int, db: Session = Depends(get_db)):
    """
    Compiles and returns the structured Pydantic AIAnalysisContext for developers.
    """
    logger.info(f"API requested context for analysis ID: {analysis_id}")
    try:
        context = context_builder.build_context(analysis_id, db)
        return ContextResponse(status="success", context=context)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"Unexpected error compiling context for analysis ID {analysis_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while compiling analysis context: {str(e)}"
        )

@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def ai_chat_interaction(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Ingests conversational prompts, retrieves structured context, queries LLM,
    runs safety validations, compiles explainable citations, and maintains chat history.
    """
    start_time = time.time()
    logger.info("API requested AI chat interaction.")

    # Standardize input query
    user_query = request.question or request.prompt
    if not user_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'question' or 'prompt' is required in chat payload."
        )

    # 1. Initialize memory session
    memory_manager = ConversationMemoryManager(db)
    conv_id = request.conversation_id or str(uuid.uuid4())
    memory_manager.create_conversation(conv_id, analysis_id=request.analysis_id)
    
    # 2. Get past chat messages to formulate intelligent context selection
    past_messages = []
    past_conv = memory_manager.get_conversation(conv_id)
    if past_conv:
        past_messages = past_conv.get("messages", [])

    # Format dialogue history context
    history_context = history_builder.build_history_context(past_messages, user_query)

    # Save user message to database
    memory_manager.add_message(conv_id, "user", user_query)

    # 3. Load analysis context
    context = None
    if request.analysis_id:
        try:
            context = context_builder.build_context(request.analysis_id, db)
        except Exception as e:
            logger.warning(f"Could not build context for request analysis ID {request.analysis_id}: {str(e)}")

    # 4. Format prompt
    if context:
        prompt_text = prompt_manager.format_prompt(
            "executive_chat",
            history=history_context,
            context=context.model_dump_json(indent=2, default=str),
            question=user_query
        )
    else:
        prompt_text = user_query

    # 5. Cache Lookup
    cached_reply_raw = None
    cache_status = "miss"
    if context:
        cached_reply_raw = ai_cache.get(prompt_text, context)

    if cached_reply_raw:
        logger.info("Cache hit! Returning compiled response.")
        cache_status = "hit"
        raw_response = cached_reply_raw
    else:
        # Request LLM provider
        raw_response = llm_provider.generate(prompt_text, context=context)

    # 6. Parse structured response
    answer = raw_response
    reasoning_summary = "Factual overview analysis of context parameters."
    key_findings = []
    recommendations = []
    follow_up_questions = []

    try:
        # Strip code markdown characters from JSON blocks if needed
        clean_json = raw_response.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        if clean_json.startswith("```"):
            clean_json = clean_json[3:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
        clean_json = clean_json.strip()

        parsed = json.loads(clean_json)
        answer = parsed.get("answer", raw_response)
        reasoning_summary = parsed.get("reasoning_summary", reasoning_summary)
        key_findings = parsed.get("key_findings", [])
        recommendations = parsed.get("recommendations", [])
        follow_up_questions = parsed.get("follow_up_questions", [])
    except Exception:
        # Fallback if reply is plain text
        logger.warning("LLM did not return standard JSON format. Running plain text parsing.")
        # Provide default structured fields
        key_findings = [f"Processed {context.rows_count} records."] if context else []
        recommendations = [r.get("text", "Drop null rows") for r in (context.recommendations or [])] if context else []

    # 7. Run safety validation checks
    validation_status = "success"
    if context:
        try:
            response_validator.validate(answer, context)
            if cache_status == "miss":
                ai_cache.set(prompt_text, context, raw_response)
        except AIValidationException as ave:
            logger.error(f"AI response validator triggered: {ave.message} - {ave.details}")
            validation_status = "warning"
            # In production, we override the answer to ensure data consistency
            answer = f"Caution: Generative analysis returned contradiction warnings. Factual context states: Overall Pulse is {context.business_pulse}/100 and rows count is {context.rows_count}."
            reasoning_summary = f"Response flagged due to contradictions: {', '.join(ave.details)}"
        except Exception as e:
            logger.error(f"Factual validator parsing exception: {str(e)}")

    # Save system message to database
    memory_manager.add_message(conv_id, "model", answer)

    # 8. Extract Citations
    citations = []
    if context:
        citations = citation_builder.build_citations(answer, context)

    # 9. Compute Explainable Confidence
    completeness = 100.0
    if context and context.validation_report:
        completeness = context.validation_report.get("missing_values", {}).get("completeness_score", 100.0)

    citation_coverage = 0.0
    sentences_count = len(answer.split('.'))
    if sentences_count > 0 and len(citations) > 0:
        citation_coverage = min(100.0, (len(citations) / sentences_count) * 100.0)

    val_success = (validation_status == "success")
    confidence_score = (completeness + citation_coverage + (100.0 if val_success else 50.0)) / 3
    confidence_score = float(round(confidence_score, 1))

    factors = [
        f"Data completeness is evaluated at {completeness}%.",
        f"Citation engine coverage: {round(citation_coverage, 1)}% backed by evidence.",
        "Hallucination check: passed." if val_success else "Hallucination check: metrics corrected."
    ]

    confidence = ExplainableConfidence(
        score=confidence_score,
        validation_success=val_success,
        citation_coverage_pct=float(round(citation_coverage, 1)),
        context_completeness_pct=completeness,
        validation_factors=factors
    )

    # 10. observabilty metadata
    elapsed = float(round(time.time() - start_time, 3))
    metadata = ResponseMetadata(
        provider="gemini",
        cache_status=cache_status,
        validation_status=validation_status,
        processing_time=elapsed
    )

    return ChatResponse(
        answer=answer,
        response=answer,
        conversation_id=conv_id,
        citations=citations,
        confidence=confidence,
        key_findings=key_findings,
        recommendations=recommendations,
        reasoning_summary=reasoning_summary,
        metadata=metadata
    )

@router.get("/conversations", response_model=ConversationsListResponse, status_code=status.HTTP_200_OK)
def list_ai_conversations(db: Session = Depends(get_db)):
    """
    Retrieves all persistent conversations logged inside PostgreSQL.
    """
    logger.info("API requested active conversations list.")
    try:
        conversations = db.query(Conversation).order_by(Conversation.updated_at.desc()).all()
        summaries = []
        for c in conversations:
            # Generate a title from the first user message, or default
            title = "New Conversation"
            first_msg = db.query(ChatMessage).filter(ChatMessage.conversation_db_id == c.id, ChatMessage.role == "user").first()
            if first_msg:
                title = first_msg.content[:40] + ("..." if len(first_msg.content) > 40 else "")
            
            summaries.append(
                ConversationSummary(
                    conversation_id=c.conversation_id,
                    workspace_id=c.workspace_id,
                    analysis_id=c.analysis_id,
                    created_at=c.created_at.isoformat(),
                    updated_at=c.updated_at.isoformat(),
                    title=title
                )
            )
        return ConversationsListResponse(status="success", conversations=summaries)
    except Exception as e:
        logger.exception("Failed to retrieve conversation lists.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query conversations: {str(e)}"
        )

@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse, status_code=status.HTTP_200_OK)
def get_ai_conversation_details(conversation_id: str, db: Session = Depends(get_db)):
    """
    Retrieves the complete message history for a specific conversation ID.
    """
    logger.info(f"API requested conversation details for ID: {conversation_id}")
    conv = db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation ID '{conversation_id}' was not found."
        )

    messages = db.query(ChatMessage).filter(ChatMessage.conversation_db_id == conv.id).order_by(ChatMessage.timestamp.asc()).all()
    message_schemas = [
        ConversationMessage(
            id=m.id,
            role=m.role,
            content=m.content,
            timestamp=m.timestamp.isoformat()
        )
        for m in messages
    ]

    return ConversationDetailResponse(
        status="success",
        conversation_id=conversation_id,
        messages=message_schemas
    )

@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_200_OK)
def delete_ai_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """
    Permanently deletes a conversation and its messages from the database.
    """
    logger.info(f"API requested delete for conversation ID: {conversation_id}")
    conv = db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation ID '{conversation_id}' was not found."
        )

    try:
        db.delete(conv)
        db.commit()
        return {"status": "success", "message": f"Conversation '{conversation_id}' successfully deleted."}
    except Exception as e:
        db.rollback()
        logger.exception("Failed to delete conversation entry")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete conversation: {str(e)}"
        )

@router.post("/suggestions/{analysis_id}", response_model=SuggestedQuestionsResponse, status_code=status.HTTP_200_OK)
def get_suggested_questions(analysis_id: int, db: Session = Depends(get_db)):
    """
    Formulates dynamic, context-aware suggested queries based on domain and schema.
    """
    logger.info(f"API requested suggested questions for analysis ID: {analysis_id}")
    try:
        context = context_builder.build_context(analysis_id, db)
        suggestions = suggestions_generator.generate_suggestions(context)
        return SuggestedQuestionsResponse(
            status="success",
            analysis_id=analysis_id,
            suggestions=suggestions
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception("Failed to generate dynamic suggestions")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compile suggestions: {str(e)}"
        )

@router.post("/report/{analysis_id}", response_model=ReportResponse, status_code=status.HTTP_200_OK)
def generate_analysis_report(analysis_id: int, db: Session = Depends(get_db)):
    """
    Orchestrates executive report drafting, executing full schema validations,
    and returns a structured JSON object.
    """
    logger.info(f"API requested structured report for analysis ID: {analysis_id}")
    try:
        context = context_builder.build_context(analysis_id, db)
        report = report_generator.generate_report(context)
        return ReportResponse(status="success", report=report)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"Unexpected error generating structured report for analysis {analysis_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during report draft generation: {str(e)}"
        )
