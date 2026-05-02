from app.models.products import Product
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def find_product(db: Session, product_id: int):
    
    product = (db.query(Product).filter(Product.id == product_id, Product.is_active.is_(True)).first())

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    return product

def find_products(db: Session, product_ids: list[int]):

    if not product_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No products provided")
    
    
    products = (db.query(Product).filter(Product.id.in_(product_ids), 
                                        Product.is_active.is_(True))
                                        .all)()
    
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product found")
    
    if len(products) != len(product_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Some products are invalid")
    
    return products

def total_price_of_products(db: Session, product_ids: list[int]):

    if not product_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No products provided")
    
    total_price = (db.query(sum(Product.price)).filter(Product.id.in_(product_ids),
                                                       Product.is_active.is_(True)).first())
    
    if not total_price:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No price found")
    
    return total_price