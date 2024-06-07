from uuid import UUID

import fastapi_jsonrpc as jsonrpc
from pydantic import BaseModel
from bookmytea_auth.app.core.jwt import register, login, verify_token


class LoginResponse(BaseModel):
    token: str


class VerifyResponse(BaseModel):
    user_id: str


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
    user_id = verify_token(token)
    if user_id:
        return VerifyResponse(user_id=user_id)
    else:
        raise VerificationError
