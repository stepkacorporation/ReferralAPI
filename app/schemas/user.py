from pydantic import BaseModel, ConfigDict, EmailStr

from datetime import datetime

from app.schemas.referral_code import ReferralCodeResponseSchema


class UserCreateSchema(BaseModel):
    email: EmailStr
    password_hash: str
    referred_by: int | None = None


class UserUpdateSchema(BaseModel):
    email: EmailStr | None = None
    password_hash: str | None = None
    referred_by: int | None = None


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    referral_code: ReferralCodeResponseSchema | None = None
    referrals: list[ReferralCodeResponseSchema] = []

    model_config = ConfigDict(from_attributes=True)
