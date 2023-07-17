from datetime import datetime
from typing import List, Dict, Optional, Union
import re

from pydantic_core.core_schema import FieldValidationInfo
from pydantic import BaseModel, EmailStr, Field, ValidationError, validator, field_validator, root_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.constants import Coauthors
from src.validators import adviser_validate, app_role_validate, coauthors_validate, fio_validate, id_validate, submitted_timemark, telephone_number_validate, updated_timemark

# telegram_id and discord_id оставить строками, так как предполагается использование int64
# TODO написать тесты для проверки валидации и заполнения данными


class ApplicationBase(BaseModel):
    telegram_id: Optional[str] = None
    discord_id: Optional[str] = None
    email: EmailStr
    phone: Optional[PhoneNumber] = None
    name: str
    surname: str
    patronymic: str
    university: str
    student_group: Optional[str] = None
    title: str
    adviser: str
    coauthors: Coauthors = None
    application_role: str
    submitted_at: str
    updated_at: str
    
    tg_id_validation = field_validator("telegram_id")(id_validate)
    ds_id_validation = field_validator("discord_id")(id_validate)
    phone_validation = field_validator("phone")(telephone_number_validate)
    name_validation = field_validator("name")(fio_validate)
    surname_validation = field_validator("surname")(fio_validate)
    patronymic_validation = field_validator("patronymic")(fio_validate)
    adviser_validation = field_validator("adviser")(adviser_validate)
    coauthors_validation = field_validator("coauthors")(coauthors_validate)
    application_role_validate = field_validator("application_role")(app_role_validate)
    get_creation_time = field_validator("submitted_at")(submitted_timemark)
    get_update_time = field_validator("updated_at")(updated_timemark)
        

class ApplicationCreate(ApplicationBase):
    pass


class Application(ApplicationBase):
    id: int


class ApplicationUpdate(ApplicationBase):
    id: int
