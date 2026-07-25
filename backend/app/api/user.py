from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.security import hash_password

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ----------------------------
# CREATE USER
# ----------------------------
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    existing_email = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ----------------------------
# GET ALL USERS
# ----------------------------
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# ----------------------------
# GET SINGLE USER
# ----------------------------
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user


# ----------------------------
# UPDATE USER
# ----------------------------
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    updated: UserUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    user.username = updated.username
    user.email = updated.email

    db.commit()
    db.refresh(user)

    return user


# ----------------------------
# DELETE USER
# ----------------------------
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }