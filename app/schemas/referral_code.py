from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, field_validator


class ReferralCodeCreateSchema(BaseModel):
    code: str
    expiry_date: datetime

    @field_validator('expiry_date')
    @classmethod
    def check_password_complexity(cls, v: datetime) -> datetime:
        if v <= datetime.now(timezone.utc):
            raise ValueError('expiry_date must be greater than the current UTC time')
        return v


class ReferralCodeUpdateSchema(BaseModel):
    code: str | None = None
    expiry_date: datetime | None = None

    @field_validator('expiry_date')
    @classmethod
    def check_password_complexity(cls, v: datetime) -> datetime | None:
        if v and v <= datetime.now(timezone.utc):
            raise ValueError('expiry_date must be greater than the current UTC time')
        return v


class ReferralCodeResponseSchema(BaseModel):
    id: int
    code: str
    expiry_date: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)
