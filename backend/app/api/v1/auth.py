from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserRead
from app.services.auth import create_access_token, hash_password, verify_password

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """Self-registration always creates a read-only employee account."""
    exists = db.query(User).filter((User.username == data.username) | (User.email == data.email)).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=UserRole.EMPLOYEE,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return Token(access_token=create_access_token(subject=str(user.id)))


@router.get("/me", response_model=UserRead)
def me(user: User = Depends(get_current_user)):
    return user
