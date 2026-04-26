from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, Float
from app.db.base import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("cart.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

