from datetime import datetime, timedelta
from typing import Optional
from app.models import TokenResponse, UserCreate, UserResponse
import jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from app.database import accounts_collection
from fastapi import Depends, HTTPException, APIRouter, Request, Response
from fastapi.security import  OAuth2PasswordRequestForm, APIKeyHeader
from datetime import timedelta
from bson import ObjectId




# Load biến môi trường
load_dotenv()
router = APIRouter()
oauth2_scheme = APIKeyHeader(name="Authorization", auto_error=False)

# Secret key cho JWT
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Cấu hình bcrypt để hash mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hàm hash mật khẩu
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Hàm kiểm tra mật khẩu
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Hàm tạo JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Hàm giải mã JWT token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    

async def check_user_exists1(username: str) -> Optional[dict]:
    return await accounts_collection.find_one({"username": username})

async def check_user_exists2(email: str) -> Optional[dict]:
    return await accounts_collection.find_one({"email": email})


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    if await check_user_exists2(user.email):
        raise HTTPException(status_code=400, detail="Email đã được sử dụng!")
    
    if await check_user_exists1(user.username):
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã được sử dụng!")
    
    hashed_password = hash_password(user.password)
    new_user = {"username": user.username, "email": user.email, "password": hashed_password}
    result = await accounts_collection.insert_one(new_user)
    
    return UserResponse(email = user.email, username=user.username)


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), response: Response = Response()):
    user = await check_user_exists1(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Tên đăng nhập hoặc mật khẩu không đúng!")

    token_data = {"sub": user["email"], "id": str(user["_id"])}
    access_token = create_access_token(token_data, timedelta(minutes=30))

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,  # Token sống 30 phút
    )

    return TokenResponse(access_token=access_token, token_type="bearer", message="Đăng nhập thành công!")



@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Đã đăng xuất!"}




async def get_current_user(request: Request):
    # Lấy token từ Cookie
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Vui lòng đăng nhập!")

    # Tách "Bearer " khỏi token
    token = token.replace("Bearer ", "")

    payload = decode_access_token(token)
    if not payload or "id" not in payload:
        raise HTTPException(status_code=401, detail="Token không hợp lệ!")

    user = await accounts_collection.find_one({"_id": ObjectId(payload["id"])})
    if not user:
        raise HTTPException(status_code=401, detail="Không tìm thấy người dùng!")

    return UserResponse(id=str(user["_id"]), username=user["username"], email=user["email"])

@router.get("/me", response_model=UserResponse)
async def get_user_info(current_user: UserResponse = Depends(get_current_user)):
    return current_user
