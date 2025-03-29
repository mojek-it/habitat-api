from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, validator
import re


class PetitionSignatureBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=5, max_length=20)
    email_consent: bool = False
    phone_consent: bool = False

    @validator("phone_number")
    def validate_phone_number(cls, v):
        # Simple validation for phone number with country code
        if not re.match(r"^\+?[0-9]{5,20}$", v):
            raise ValueError(
                "Invalid phone number format. Must include country code (e.g., +1234567890)"
            )
        return v


class PetitionSignatureCreate(PetitionSignatureBase):
    pass


class PetitionSignatureResponse(PetitionSignatureBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True


class PetitionBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    target: int = Field(..., gt=0)
    email_subject: str = Field(..., min_length=3, max_length=255)
    email_content: str = Field(..., min_length=10)


class PetitionCreate(PetitionBase):
    pass


class PetitionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    target: Optional[int] = Field(None, gt=0)
    signature_count: Optional[int] = Field(None, ge=0)
    email_subject: Optional[str] = Field(None, min_length=3, max_length=255)
    email_content: Optional[str] = Field(None, min_length=10)


class PetitionResponse(PetitionBase):
    id: int
    signature_count: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class PetitionDetailResponse(PetitionResponse):
    signatures: List[PetitionSignatureResponse] = []

    class Config:
        orm_mode = True
