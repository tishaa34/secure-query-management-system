from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import AuditAction
from app.db.session import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    query_id: Mapped[int] = mapped_column(ForeignKey("queries.id"), nullable=False, index=True)
    action: Mapped[AuditAction] = mapped_column(Enum(AuditAction, name="audit_action_enum"), nullable=False)
    performed_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    query = relationship("Query", back_populates="audit_logs")
    performed_by = relationship("User", back_populates="audit_entries")
