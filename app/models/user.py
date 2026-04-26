from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from app.db.base import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    cart = relationship("Cart", back_populates="user", uselist=False, foreign_keys="Cart.user_id")
    orders = relationship("Order", back_populates="user")