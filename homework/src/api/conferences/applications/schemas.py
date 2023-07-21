from typing import Optional

from pydantic import BaseModel

__all__ = ('UserSchema', 'UpdateUserSchema')


class _CoauthorSchema(BaseModel):
    name: str
    surname: str
    patronymic: str


class UserSchema(BaseModel):
    id: str | None = None
    telegram_id: str | None = None
    discord_id: str | None = None
    email: str
    phone: str | None = None
    name: str
    surname: str
    patronymic: str
    university: str
    student_group: str | None = None
    title: str
    adviser: str
    applicant_role: str
    submitted_at: str | None = None
    updated_at: str | None = None
    coauthors: list[_CoauthorSchema] | None = None


class UpdateUserSchema(UserSchema):
    id: str | None = None
    telegram_id: str | None = None
    discord_id: str | None = None
    email: str | None = None
    phone: str | None = None
    name: str | None = None
    surname: str | None = None
    patronymic: str | None = None
    university: str | None = None
    student_group: str | None = None
    title: str | None = None
    adviser: str | None = None
    applicant_role: str | None = None
    submitted_at: str | None = None
    updated_at: str | None = None
    coauthors: list[_CoauthorSchema] | None = None
