import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
import threading

from app.models.ai_memory import Conversation, ChatMessage

logger = logging.getLogger("conversation_memory")

class ConversationMemoryManager:
    """
    Manages chat histories, persisting to PostgreSQL with thread-safe fallback.
    """
    _in_memory_store: Dict[str, Dict[str, Any]] = {}
    _lock = threading.Lock()

    def __init__(self, db: Optional[Session] = None):
        self.db = db
        # Automatically determine mode
        self.db_active = False
        if self.db is not None:
            try:
                # Basic connection test or check if table query runs
                self.db.query(Conversation).first()
                self.db_active = True
                logger.info("Conversation Memory running in PostgreSQL mode.")
            except Exception:
                logger.warning("PostgreSQL tables not ready or session unconfigured. Falling back to In-Memory mode.")

    def create_conversation(self, conversation_id: str, workspace_id: Optional[int] = None, analysis_id: Optional[int] = None) -> Dict[str, Any]:
        logger.info(f"Creating conversation: {conversation_id} (PostgreSQL: {self.db_active})")
        
        if self.db_active and self.db:
            try:
                # Check if it already exists
                existing = self.db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
                if existing:
                    return existing.to_dict()

                conv = Conversation(
                    conversation_id=conversation_id,
                    workspace_id=workspace_id,
                    analysis_id=analysis_id
                )
                self.db.add(conv)
                self.db.commit()
                self.db.refresh(conv)
                return conv.to_dict()
            except Exception as e:
                logger.error(f"Failed to save conversation to DB: {str(e)}. Reverting to in-memory.")
                # Fallback to memory
                
        with self._lock:
            if conversation_id not in self._in_memory_store:
                self._in_memory_store[conversation_id] = {
                    "conversation_id": conversation_id,
                    "workspace_id": workspace_id,
                    "analysis_id": analysis_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                    "messages": []
                }
            return self._in_memory_store[conversation_id]

    def add_message(self, conversation_id: str, role: str, content: str) -> Dict[str, Any]:
        logger.info(f"Adding chat message from role '{role}' to conversation '{conversation_id}'")
        
        if self.db_active and self.db:
            try:
                conv = self.db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
                if not conv:
                    # Auto-create if missing
                    conv = Conversation(conversation_id=conversation_id)
                    self.db.add(conv)
                    self.db.commit()
                    self.db.refresh(conv)

                msg = ChatMessage(
                    conversation_db_id=conv.id,
                    role=role,
                    content=content
                )
                self.db.add(msg)
                conv.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(msg)
                return msg.to_dict()
            except Exception as e:
                logger.error(f"Failed to append message in DB: {str(e)}. Using in-memory fallback.")
                
        with self._lock:
            if conversation_id not in self._in_memory_store:
                self.create_conversation(conversation_id)
                
            msg_dict = {
                "id": len(self._in_memory_store[conversation_id]["messages"]) + 1,
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow().isoformat()
            }
            self._in_memory_store[conversation_id]["messages"].append(msg_dict)
            self._in_memory_store[conversation_id]["updated_at"] = datetime.utcnow().isoformat()
            return msg_dict

    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        logger.info(f"Retrieving conversation details for conversation ID: {conversation_id}")
        
        if self.db_active and self.db:
            try:
                conv = self.db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
                if conv:
                    return conv.to_dict()
                return None
            except Exception as e:
                logger.error(f"Failed to query conversation from DB: {str(e)}")
                
        with self._lock:
            return self._in_memory_store.get(conversation_id)
            
    def list_conversations(self) -> List[Dict[str, Any]]:
        logger.info("Listing all active conversations...")
        
        if self.db_active and self.db:
            try:
                convs = self.db.query(Conversation).all()
                return [c.to_dict() for c in convs]
            except Exception as e:
                logger.error(f"Failed to list conversations from DB: {str(e)}")
                
        with self._lock:
            return list(self._in_memory_store.values())
