from datetime import datetime

from sqlalchemy import DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import Role
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    role: Mapped[Role] = mapped_column(Enum(Role, name="role_enum"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    created_queries = relationship("Query", foreign_keys="Query.created_by_id", back_populates="created_by")
    assigned_queries = relationship("Query", foreign_keys="Query.assigned_to_id", back_populates="assigned_to")
    audit_entries = relationship("AuditLog", back_populates="performed_by")
