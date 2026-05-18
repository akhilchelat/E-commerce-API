from app.db.base import Base
from app.models.order import OrderStatus
from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SqlEnum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum

class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    old_status = Column(SqlEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    new_status = Column(SqlEnum(OrderStatus), nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    order = relationship("Order", back_populates="order_status_history")