from app.models.products import Product
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def find_product(db: Session, product_id: int):
    
    product = (db.query(Product).filter(Product.id == product_id, Product.is_active.is_(True)).first())

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    return product
