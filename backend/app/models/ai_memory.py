from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

# Ensure SQLAlchemy registers dependent tables in metadata
from app.models.workspace import Workspace
from app.models.analysis_result import AnalysisResult

class Conversation(Base):
    __tablename__ = "ai_conversations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    conversation_id = Column(String, unique=True, index=True, nullable=False)
    workspace_id = Column(Integer, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=True)
    analysis_id = Column(Integer, ForeignKey("analysis_results.id", ondelete="CASCADE"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    messages = relationship("ChatMessage", back_populates="conversation", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "workspace_id": self.workspace_id,
            "analysis_id": self.analysis_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "messages": [m.to_dict() for m in self.messages]
        }

class ChatMessage(Base):
    __tablename__ = "ai_chat_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    conversation_db_id = Column(Integer, ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False)  # "user", "model", "system"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
