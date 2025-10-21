from sqlalchemy import Column, Integer, String, Enum, DateTime, func, Boolean
import enum

from app.database.base import Base

class Role(str, enum.Enum):
    user = "USER"
    admin = "ADMIN"

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(55))
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    password = Column(String)
    role = Column(Enum(Role), default=Role.user, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    is_verified = Column(Boolean, default=False)
    # verification code is storing here in Users model
    verification_code = Column(String(4))
    verification_code_created_at = Column(DateTime(timezone=True), server_default=func.now())

