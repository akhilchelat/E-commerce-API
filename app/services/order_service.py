from app.models.order import Order, OrderStatus
from app.models.orderitem import OrderItem
from app.models.cartitem import CartItem
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.repeating_functions.user_functions import find_user
from app.repeating_functions.cart_functions import get_selected_cart_items, deactivate_cart_items
from app.repeating_functions.order_functions import get_order, get_orderitems_from_order

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

        deactivate_cart_items(cart_items)    

        db.commit()
        db.refresh(new_order)
                                                                         
        return new_order
            
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="order already exist")
    
    except HTTPException:
        db.rollback()
        raise
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="something went wrong")


def get_order_by_id(db: Session, user_id: int, order_id: int):

    order = get_order(db, user_id, order_id)

    return order

def get_user_orders(db: Session, user_id: int):  

    find_user(db, user_id)

    orders = (db.query(Order).filter(Order.user_id == user_id,
                                     Order.is_active.is_(True))
                                     .order_by(Order.created_at.desc())
                                     .all())

    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No order found")

    return orders  


def cancel_order(db: Session, user_id: int, order_id: int):

    find_user(db, user_id)

    order_item = get_orderitems_from_order(db, user_id, order_id)

    order = get_order(db, user_id, order_id)

    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="only pending orders can be cancelled")
    
    order.is_active = False
    order.status = OrderStatus.CANCELLED    

    for item in order_item:
        item.is_active = False
        item.product.stock += item.quantity
    
    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="something went wrong")

    except HTTPException:
        db.rollback()
        raise
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="something went wrong")





                  
# {
#   "id": 1,
#   "user_id": 5,
#   "total_price": 2500,
#   "status": "PENDING",
#   "items": [
#     {
#       "product_id": 2,
#       "quantity": 1,
#       "price": 1500
#     },
#     {
#       "product_id": 4,
#       "quantity": 2,
#       "price": 500
#     }
#   ]
# }
    



     















    
