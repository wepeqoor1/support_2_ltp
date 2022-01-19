from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from app.controllers import (
    user_login,
    get_user_in_db,
    get_scratchcards,
    get_scratchcards_number,
    get_stat_fiscal_doc_sender_queue_unloading_checks,
    get_stat_fiscal_doc_sender_queue_user_inn,
    get_stat_fiscal_doc_sender_queue_user_email,
    get_kkt_for_fn,
    get_kkt_for_rnm,
    get_kkt_for_zn,
    get_super_user_login_password,
)


SECRET_KEY = "901af50c1f9aaa353e78e0d99ee77b7a6f272c2e57af8338802e1926afb8d99f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    password: Optional[str] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(username: str):
    user_dict = get_user_in_db(login=username)
    if user_dict:
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str):
    user: dict = user_login(username, password)
    if not user:
        return False
    return UserInDB(**user)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/api/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/api/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/api/users/scratchcard/{scratchcard_code}")
async def scratchcard(
    scratchcard_code: str, current_user: User = Depends(get_current_active_user)
):
    result = get_scratchcards(str(scratchcard_code))
    return result


@router.get("/api/users/scratchcard_number/{scratchcard_number}")
async def scratchcard_number(
    scratchcard_number: str, current_user: User = Depends(get_current_active_user)
):
    result = get_scratchcards_number(str(scratchcard_number))
    return result


@router.get("/api/users/stat_fiscal_doc_sender_queue/user_mail/{user_mail}")
async def stat_fiscal_doc_sender_queue_user_mail(
    user_mail: str, current_user: User = Depends(get_current_active_user)
):
    result = get_stat_fiscal_doc_sender_queue_user_email(str(user_mail))

    return result


@router.get("/api/users/stat_fiscal_doc_sender_queue/user_inn/{user_inn}")
async def stat_fiscal_doc_sender_queue_user_inn(
    user_inn: str, current_user: User = Depends(get_current_active_user)
):
    result = get_stat_fiscal_doc_sender_queue_user_inn(str(user_inn))

    return result


@router.get("/api/users/stat_fiscal_doc_sender_queue/")
async def stat_fiscal_doc_sender_queue(
    current_user: User = Depends(get_current_active_user),
):
    result = get_stat_fiscal_doc_sender_queue_unloading_checks()

    return result


@router.get("/api/users/kkt/rnm/{rnm}")
async def kkt_for_rnm(
    rnm: str,
    current_user: User = Depends(get_current_active_user),
):
    result = get_kkt_for_rnm(rnm)

    return result


@router.get("/api/users/kkt/fn/{fn}")
async def kkt_for_fn(
    fn: str,
    current_user: User = Depends(get_current_active_user),
):
    result = get_kkt_for_fn(fn)

    return result


@router.get("/api/users/kkt/zn/{zn}")
async def kkt_for_zn(
    zn: str,
    current_user: User = Depends(get_current_active_user),
):
    result = get_kkt_for_zn(zn)

    return result


@router.get("/api/users/super_user_login_password/{user_inn}")
async def super_user_login_password(
    user_inn: str,
    current_user: User = Depends(get_current_active_user),
):
    result = get_super_user_login_password(user_inn) 

    return result