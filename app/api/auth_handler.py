# auth.py
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import app.auth.security as auth_utils
import app.auth.requests_rq as rq
from app.schemas.auth_schemas import UserSchema

http_bearer = HTTPBearer()

auth_router = APIRouter()

async def validate_auth_user(username: str = Form(), password: str = Form()):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password")
    user = await rq.get_user(username)
    if user==None:
        raise unauthed_exc

    if not auth_utils.validate_password(password=password, hashed_password=user.hashed_password):
        raise unauthed_exc

    return user


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> dict:
    token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(token=token)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError:  # ← вместо DecodeError
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

async def get_current_auth_user(payload: dict = Depends(get_current_token_payload)) -> UserSchema:
    username: str | None = payload.get("sub")
    user = await rq.get_user(username)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid (user not found)",)


@auth_router.post("/login/")
async def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user)):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
    }
    token = auth_utils.encode_jwt(jwt_payload)

    return {
        "access_token": token,
        "token_type": "Bearer",
        "username": user.username,  # можно сразу дать фронту
    }


@auth_router.get("/users/me/")
def auth_user_check_self_info(payload: dict = Depends(get_current_token_payload), user: UserSchema = Depends(get_current_auth_user)):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "logged_in_at": iat,
    }

@auth_router.post("/register/")
async def register_user(username: str = Form(), password: str = Form()):
    hashed_password = auth_utils.hash_password(password)
    await rq.create_user(username=username, hashed_password=hashed_password)

    return {
        "detail": "User registered successfully."
    }
