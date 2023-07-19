from datetime import datetime
from typing import Optional
import re

from src.constants import Coauthors, RE_LINE_ID, RE_LINE_ADVISER, RE_LINE_FIO, APPLICATION_ROLES


def id_validate(val: Optional[str]):
    """
    Валидация id
    """
    if val:
        pattern = re.compile(RE_LINE_ID)
        if pattern.match(val):
            return val
        else:
            raise ValueError('must contain only digits')


def telephone_number_validate(val: str):
    """
    Валидация номера телефона
    """
    if val:
        if val.find("tel:") != -1:
            val = val[4:]
            
        return val


def fio_validate(val: str):
    """
    Валидация для полей ФИО
    """
    if val:
            pattern = re.compile(RE_LINE_FIO)
            if pattern.match(val):
                return val
            else:
                raise ValueError("must contain only russian letters and '-'")
            

def app_role_validate(val: str):
    """
    Валидация поля application_role
    """
    if val:
            if val in APPLICATION_ROLES:
                return val
            else:
                raise ValueError(f"Application role must be {APPLICATION_ROLES}")
  

def adviser_validate(val: str):
    """
    Валидация поля adviser
    """
    if val:
        pattern = re.compile(RE_LINE_ADVISER)
        if pattern.match(val):
            return val
        else:
            raise ValueError("Adviser name must contain only russian letters and '-', '.'")


def coauthors_validate(val: Coauthors):
    """
    Валидация поля coauthors
    """
    if val:
        for coauthor in val:
            fields = list(coauthor.items())
            if fields:
                for field in fields:
                    if field[1]:
                        tmp = fio_validate(val=field[1])
                    else:
                        raise ValueError(f"Coauthor's {field[0]} can't be empty")   
            else:
                raise ValueError("Coauthor field can't be empty")
        return val
    

def submitted_timemark(val: str):
    """
    Валидация временных полей
    """
    if val:
        try:
            datetime.fromisoformat(val)
            return val
        except ValueError:
            raise ValueError("date must be represented in ISO 8601 form")
    else:
        raise ValueError("No submite time")


def updated_timemark(val: str):
    """
    Обновление времени
    """
    return datetime.now().astimezone().isoformat()

