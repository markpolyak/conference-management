# from datetime import datetime
from typing import List, Dict

from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


# telegram_id and discord_id оставить строками, так как предполагается использование int64
# TODO для остральных полей сделать валидацию
# TODO написать тесты для проверки валидации и заполнения данными
# TODO понять как работать с гугл шит и понять структуру таблиц

class ApplicationBase(BaseModel):
    telegram_id: str | None
    discord_id: str | None
    email: EmailStr
    phone: PhoneNumber | None
    name: str
    surname: str
    patronymic: str
    university: str
    student_group: str | None
    title: str
    adviser: str
    coauthors: List[Dict[str, str]] | None

    def trim_phone(self):
        if self.phone:
            self.phone = self.phone[4:]


class ApplicationCreate(ApplicationBase):
    pass


class Application(ApplicationBase):
    id: int
    