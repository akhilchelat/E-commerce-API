from app.models.order import Order
from app.models.orderitem import OrderItem
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repeating_functions.user_functions import find_user

def get_order(db: Session, user_id: int, order_id: int):

    if user_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid user_id")
    
    if order_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid order_id")
    
    find_user(db, user_id)

    order = (db.query(Order).filter
                   (Order.id == order_id,
                    Order.user_id == user_id,
                    Order.is_active.is_(True)).first())
    
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no order exist")

    return order 

def get_orderitems_from_order(db: Session, user_id: int, order_id: int):

    find_user(db, user_id)

    order_items = (db.query(OrderItem).filter(OrderItem.order_id == order_id,
                                              OrderItem.is_active.is_(True)).all())
    
    if not order_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No item found")
    
    return order_items