from app.models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def find_user(db: Session, user_id: int):

    user = (db.query(User).filter(User.id == user_id, User.is_active.is_(True)).first())

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user

