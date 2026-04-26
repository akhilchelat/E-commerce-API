from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.cart import Cart
from app.models.cartitem import CartItem
from app.models.products import Product
from app.repeating_functions.user_functions import find_user
from app.repeating_functions.cart_functions import find_cart
from app.repeating_functions.product_functions import find_product
from sqlalchemy.exc import IntegrityError

def create_cart(db: Session, user_id: int):
    
    find_user(db, user_id)
    
    cart = (db.query(Cart).filter(Cart.user_id == user_id).first())

    if cart:
        if not cart.is_active:
            cart.is_active = True
            db.commit()
            db.refresh(cart)
        return cart
        
    new_cart = Cart(user_id=user_id)
    db.add(new_cart)
    try:
        db.commit()
        db.refresh(new_cart)
        return new_cart
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cart already exists")
    
def add_to_cart(db: Session, cart_id: int, product_id: int, quantity: int):

    if quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be greater than 0")

    find_cart(db, cart_id)

    product = find_product(db, product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    if product.stock < quantity:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product is out of stock")

    existing_cart_product = (db.query(CartItem)
                             .filter(CartItem.product_id == product_id,
                                    CartItem.cart_id == cart_id,
                                    CartItem.is_active.is_(True)).first())
    
    if existing_cart_product:
        if existing_cart_product.quantity + quantity > product.stock:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product is out of stock")
        
        existing_cart_product.quantity += quantity
        db.commit()
        db.refresh(existing_cart_product)
        return existing_cart_product
       
    new_cart_product = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
    db.add(new_cart_product)
    db.commit()
    db.refresh(new_cart_product)

    return new_cart_product

def get_cart_by_user(db: Session, user_id: int):

    return create_cart(db, user_id)

def update_cart_item_quantity(db: Session, cart_id: int, product_id: int, quantity: int):

    if quantity < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity cannot be negative")

    find_cart(db, cart_id)
    product = find_product(db, product_id)

    cart_item = (db.query(CartItem).filter(CartItem.cart_id == cart_id,
                                           CartItem.product_id == product_id,
                                           CartItem.is_active.is_(True)).first())
    
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    
    if quantity == 0:
        cart_item.is_active = False
        db.commit()  
        db.refresh(cart_item)
        return {"message": "Item removed from cart"} 


    if quantity > product.stock:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Requested quantity exceeds available stock")
    
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

def remove_product_from_cart(db: Session, cart_id: int, product_id: int):

    find_cart(db, cart_id)
    find_product(db, product_id)
    
    cart_item = (db.query(CartItem).filter(CartItem.cart_id == cart_id, 
                                           CartItem.product_id == product_id,
                                           CartItem.is_active.is_(True)).first())
     
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    
    cart_item.is_active = False
    db.commit()
    db.refresh(cart_item)
    return {"message": "Product removed from cart"}

def clear_cart(db: Session, cart_id: int):

    find_cart(db, cart_id)
  
    cart_items = (db.query(CartItem).filter(CartItem.cart_id == cart_id, CartItem.is_active.is_(True)).all())

    if not cart_items:
        return {"message": "cart is already empty"}
    
    for product in cart_items:
        product.is_active = False

    db.commit()

    return {"message": "all products removed from cart"}    

def get_cart_items(db: Session, cart_id: int):

    find_cart(db, cart_id)

    products = (db.query(Product.name.label("name"),
                            Product.price.label("price"), 
                            Product.description.label("description"), 
                            CartItem.quantity.label("quantity"))
                    .join(Product.cart_items)
                    .filter(CartItem.cart_id == cart_id, CartItem.is_active.is_(True)).all())
    
    if not products:
        return {"message": "cart is already empty"}
        
    return [{"product_name" : product.name,
            "product_price" : product.price,
            "product_description" : product.description,
            "product_quantity" : product.quantity}
            
            for product in products
            ]

def get_cart_total(db: Session, cart_id: int):

    find_cart(db, cart_id)
    
    products = (db.query(func.sum(CartItem.quantity).label("total_quantity"),
                                   func.sum(CartItem.quantity * Product.price).label("total_price"))
                                   .join(CartItem.product)
                                   .filter(CartItem.cart_id == cart_id, CartItem.is_active.is_(True))
                                   .first()) 

    total_quantity = products.total_quantity or 0
    total_price = products.total_price or 0

    return {"total_quantity" : total_quantity,
            "total_price" : total_price} 


      
    



