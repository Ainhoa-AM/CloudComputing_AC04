from fastapi import APIRouter, Body, HTTPException, Header
from pydantic import BaseModel
from app.authentication.models import UserDB
from app.authentication.domain.persistences.token_interface import TokenInterface
from app.authentication.dependency_injection.persistences.token_persistences import TokenPersistences

import hashlib

router = APIRouter()

token_service: TokenInterface = TokenPersistences.carlemany()


class RegisterInput(BaseModel):
    username: str
    password: str
    mail: str
    year_of_birth: int


class RegisterOutput(BaseModel):
    username: str
    mail: str
    year_of_birth: int


@router.post("/register")
async def register(input: RegisterInput = Body()) -> dict[str, RegisterOutput]:
    user_exists = await UserDB.filter(username=input.username).first()
    if user_exists:
        raise HTTPException(status_code=409, detail="This username is already taken")

    hash_password = input.username + input.password
    hashed_password = hashlib.sha256(hash_password.encode()).hexdigest()

    await UserDB.create(
        username=input.username,
        password=hashed_password,
        mail=input.mail,
        year_of_birth=input.year_of_birth
    )

    output = RegisterOutput(
        username=input.username,
        mail=input.mail,
        year_of_birth=input.year_of_birth
    )
    return {"new_user": output}


class LoginInput(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(input: LoginInput = Body()) -> dict[str, str]:
    user = await UserDB.filter(username=input.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hash_password = input.username + input.password
    hashed_input_password = hashlib.sha256(hash_password.encode()).hexdigest()

    if user.password == hashed_input_password:
        token = await token_service.create_token(user.username)
        return {"auth": token}
    else:
        raise HTTPException(status_code=403, detail="Password is not correct")


class IntrospectOutput(BaseModel):
    username: str
    mail: str
    year_of_birth: int


@router.get("/introspect")
async def introspect_get(auth: str = Header()) -> IntrospectOutput:
    username = await token_service.introspect_token(auth)
    if username is None:
        raise HTTPException(status_code=403, detail="Forbidden")

    user = await UserDB.get(username=username)

    return IntrospectOutput(
        username=user.username,
        mail=user.mail,
        year_of_birth=user.year_of_birth
    )


@router.get("/logout")
async def logout(auth: str = Header()) -> dict[str, str]:
    username = await token_service.introspect_token(auth)
    if username is None:
        raise HTTPException(status_code=403, detail="Forbidden")

    await token_service.delete_token(auth)
    return {"status": "User logged out"}
