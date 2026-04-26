from app.models.cart import Cart
from app.models.cartitem import CartItem
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def find_cart(db: Session, cart_id: int):
    
    cart = (db.query(Cart).filter(Cart.id == cart_id, Cart.is_active.is_(True)).first())

    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    
    return cart

def get_selected_cart_items(db: Session, user_id: int, cart_item_ids: list[int]):

    if not cart_item_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No cart items provided")
    
    cart_item_ids = list(set(cart_item_ids))

    cart_items = (db.query(CartItem)
                  .join(Cart)
                  .filter(Cart.user_id == user_id,
                          Cart.is_active.is_(True),
                          CartItem.id.in_(cart_item_ids), 
                          CartItem.is_active.is_(True)).all())

    if not cart_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart items not found")
    
    if len(cart_items) != len(cart_item_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Some cart items are invalid")

    return cart_items
    






      




