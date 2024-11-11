from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReferralCodeCreateSchema(BaseModel):
    code: str
    expiry_date: datetime
    user_id: int


class ReferralCodeUpdateSchema(BaseModel):
    code: str | None = None
    expiry_date: datetime | None = None


class ReferralCodeResponseSchema(BaseModel):
    id: int
    code: str
    expiry_date: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)
