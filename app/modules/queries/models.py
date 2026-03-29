from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import QueryPriority, QueryStatus
from app.db.session import Base


class Query(Base):
    __tablename__ = "queries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[QueryStatus] = mapped_column(
        Enum(QueryStatus, name="query_status_enum"),
        nullable=False,
        default=QueryStatus.NEW,
        server_default=QueryStatus.NEW.value,
    )
    priority: Mapped[QueryPriority | None] = mapped_column(
        Enum(QueryPriority, name="query_priority_enum"),
        nullable=True,
    )
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    assigned_to_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    created_by = relationship("User", foreign_keys=[created_by_id], back_populates="created_queries")
    assigned_to = relationship("User", foreign_keys=[assigned_to_id], back_populates="assigned_queries")
    audit_logs = relationship("AuditLog", back_populates="query", cascade="all, delete-orphan")
