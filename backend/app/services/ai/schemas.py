from pydantic import BaseModel, Field
from typing import Optional, List
from app.services.ai.models import AIAnalysisContext, AIReport, Citation

class ExplainableConfidence(BaseModel):
    score: float = Field(..., description="Overall confidence percentage score (0-100)")
    validation_success: bool = Field(..., description="Fact check validation status")
    citation_coverage_pct: float = Field(..., description="Percentage of claims backed by backend citations")
    context_completeness_pct: float = Field(..., description="Data completeness score")
    validation_factors: List[str] = Field(default=[], description="Bullet list detailing confidence drivers")

class ResponseMetadata(BaseModel):
    provider: str = Field(..., description="Selected LLM Provider (e.g. 'gemini')")
    cache_status: str = Field(..., description="Response delivery cache state ('hit' or 'miss')")
    validation_status: str = Field(..., description="Hallucination check outcome ('success' or 'warning')")
    processing_time: float = Field(..., description="Server execution time in seconds")

class ChatRequest(BaseModel):
    question: Optional[str] = Field(None, description="User query question query string")
    prompt: Optional[str] = Field(None, description="Backward compatible alias for user query string")
    conversation_id: Optional[str] = Field(None, description="Active conversation identifier UUID")
    analysis_id: Optional[int] = Field(None, description="Active dataset analysis database ID")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="Primary explanatory answer response text")
    response: str = Field(..., description="Backward compatible prompt answer response text")
    conversation_id: str = Field(..., description="Active conversation reference index")
    citations: List[Citation] = Field(default=[], description="Structured factual engine citations")
    confidence: ExplainableConfidence = Field(..., description="Factual confidence explainability profile")
    key_findings: List[str] = Field(default=[], description="Key analytical findings discovered")
    recommendations: List[str] = Field(default=[], description="Operational decision recommendations")
    reasoning_summary: str = Field(..., description="Factual reasoning summary")
    metadata: ResponseMetadata = Field(..., description="Generative observability metadata parameters")

class ConversationMessage(BaseModel):
    id: int
    role: str
    content: str
    timestamp: str

class ConversationSummary(BaseModel):
    conversation_id: str
    workspace_id: Optional[int]
    analysis_id: Optional[int]
    created_at: str
    updated_at: str
    title: str = "New Conversation"

class ConversationDetailResponse(BaseModel):
    status: str = "success"
    conversation_id: str
    messages: List[ConversationMessage]

class ConversationsListResponse(BaseModel):
    status: str = "success"
    conversations: List[ConversationSummary]

class SuggestedQuestionsResponse(BaseModel):
    status: str = "success"
    analysis_id: int
    suggestions: List[str] = Field(..., description="List of dynamically context-derived questions")

class ContextResponse(BaseModel):
    status: str = "success"
    context: AIAnalysisContext = Field(..., description="Compiled structured analysis facts context")

class ReportResponse(BaseModel):
    status: str = "success"
    report: AIReport = Field(..., description="Structured executive decision-making analysis report")
