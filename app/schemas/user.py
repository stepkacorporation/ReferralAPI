from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator, model_serializer

from app.schemas.referral_code import ReferralCodeResponseSchema

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128
SPECIAL_CHARACTERS = r'!@#$%^&*()-_=+[]{}|;:,.<>?/'

EMAIL_DESCRIPTION = 'User\'s email address, must be a valid email'
PASSWORD_DESCRIPTION = 'User\'s password'
PASSWORD_REPEAT_DESCRIPTION = 'Repeat password to confirm'
REFERRAL_CODE_DESCRIPTION = 'Referral code of the referring user'


class PasswordValidator:
    @staticmethod
    def check_password_complexity(password: str) -> str:
        if len(password) < PASSWORD_MIN_LENGTH:
            raise ValueError(f'Password must be at least {PASSWORD_MIN_LENGTH} characters long')
        if len(password) > PASSWORD_MAX_LENGTH:
            raise ValueError(f'Password must not exceed {PASSWORD_MAX_LENGTH} characters')
        if not any(c.isupper() for c in password):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in password):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in password):
            raise ValueError('Password must contain at least one digit')
        if not any(c in SPECIAL_CHARACTERS for c in password):
            raise ValueError('Password must contain at least one special character')
        return password

    @staticmethod
    def validate_passwords_match(password1: str, password2: str) -> None:
        if password1 != password2:
            raise ValueError('Passwords do not match')


class UserCreateSchema(BaseModel):
    email: EmailStr = Field(..., description=EMAIL_DESCRIPTION)
    password: str = Field(..., description=PASSWORD_DESCRIPTION)
    password_repeat: str = Field(..., description=PASSWORD_REPEAT_DESCRIPTION)
    referral_code: str | None = Field(None, description=REFERRAL_CODE_DESCRIPTION)

    @field_validator('password')
    @classmethod
    def check_password_complexity(cls, v: str) -> str:
        return PasswordValidator.check_password_complexity(v)

    @model_validator(mode='after')
    def validate_passwords_match(self) -> Self:
        PasswordValidator.validate_passwords_match(self.password, self.password_repeat)
        return self


class UserUpdateSchema(BaseModel):
    email: EmailStr | None = Field(None, description=EMAIL_DESCRIPTION)
    password: str | None = Field(None, description=PASSWORD_DESCRIPTION)
    password_repeat: str | None = Field(None, description=PASSWORD_REPEAT_DESCRIPTION)
    referred_by: int | None = Field(None, description=REFERRAL_CODE_DESCRIPTION)

    @field_validator('password')
    @classmethod
    def check_password_complexity(cls, v: str | None) -> str | None:
        if v is not None:
            return PasswordValidator.check_password_complexity(v)
        return v

    @model_validator(mode='after')
    def validate_passwords_match(self) -> Self:
        if self.password and self.password_repeat:
            PasswordValidator.validate_passwords_match(self.password, self.password_repeat)
        return self


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
