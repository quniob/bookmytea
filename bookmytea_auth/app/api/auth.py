from uuid import UUID

import fastapi_jsonrpc as jsonrpc
from pydantic import BaseModel
from app.core.core_jwt import register, login, verify_token


class LoginResponse(BaseModel):
    token: str


class VerifyResponse(BaseModel):
    user_id: str
    admin: str


class RegistrationError(jsonrpc.BaseError):
    CODE = 1001
    MESSAGE = 'Registration error'


class LoginError(jsonrpc.BaseError):
    CODE = 1002
    MESSAGE = 'Login error'


class VerificationError(jsonrpc.BaseError):
    CODE = 1003
    MESSAGE = 'Token verification error'


common_errors = [RegistrationError, LoginError, VerificationError]
common_errors.extend(jsonrpc.Entrypoint.default_errors)
api_entrypoint = jsonrpc.Entrypoint(
    '/api/v1/jsonrpc/auth',
    errors=common_errors,
)


@api_entrypoint.method(errors=[RegistrationError])
def register_user(email: str, password: str, uuid: str) -> LoginResponse:
    result = register(email, password, uuid)
    if result:
        token = login(email, password)
        return LoginResponse(token=token)
    raise RegistrationError


@api_entrypoint.method(errors=[LoginError])
def login_user(email: str, password: str) -> LoginResponse:
    token = login(email, password)
    if token:
        return LoginResponse(token=token)
    else:
        raise LoginError


@api_entrypoint.method(errors=[VerificationError])
def verify_user(token: str) -> VerifyResponse:
    payload = verify_token(token)
    user_id = payload['user_id']
    admin = payload['admin']
    if user_id:
        return VerifyResponse(user_id=user_id, admin=admin)
    else:
        raise VerificationError
