from app.models.order import Order
from app.models.orderitem import OrderItem
from app.models.cartitem import CartItem
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.repeating_functions.user_functions import find_user
from app.repeating_functions.cart_functions import get_selected_cart_items, deactivate_cart_items


def create_order(db: Session, user_id: int, cart_item_ids: list[int]):

    find_user(db, user_id)
    
    cart_items = get_selected_cart_items(db, user_id, cart_item_ids)

    total_price = 0
    
    for item in cart_items:
        if item.product.stock < item.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"product is out of stock {item.product_id}")
        
        total_price += item.product.price * item.quantity

    try:
        new_order = Order(user_id=user_id, total_price=total_price)  
    
        db.add(new_order)    
        db.flush()

        for item in cart_items:
            order_item = OrderItem(order_id=new_order.id, 
                                   product_id=item.product_id, 
                                   quantity=item.quantity, 
                                   price=item.product.price)

            db.add(order_item)

            item.product.stock -= item.quantity

        deactivate_cart_items(cart_item_ids)    

        db.commit()
        db.refresh(new_order)
                                                                         
        return new_order
            
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="order already exist")
    
    

                  


    
    



     















    
