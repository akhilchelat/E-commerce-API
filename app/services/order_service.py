from app.models.order import Order
from app.models.cartitem import CartItem
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.repeating_functions.user_functions import find_user
from app.repeating_functions.cart_functions import get_selected_cart_items


def create_order(db: Session, user_id: int, cart_item_id: list[int]):

    find_user(db, user_id)
    
    cart_items = get_selected_cart_items(db, user_id, cart_item_id)















    
