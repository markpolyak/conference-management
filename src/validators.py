from datetime import datetime
from typing import Optional
import re

from src.constants import Coauthors


def id_validate(val: Optional[str]):
        if val:
            pattern = re.compile(r"^\d+$")
            if pattern.match(val):
                return val
            else:
                raise ValueError('must contain only digits')


def telephone_number_validate(val: str):
    if val:
        if val.find("tel:") != -1:
            val = val[4:]
            
        return val


def fio_validate(val: str):
    if val:
            pattern = re.compile(r"^(?:[А-Я]|[а-я]|-)+$")
            if pattern.match(val):
                return val
            else:
                raise ValueError("must contain only russian letters and '-'")
            

def app_role_validate(val: str):
    if val:
            if val in ("студент", "аспирант", "сотрудник"): # переделать в константу
                return val
            else:
                raise ValueError("Application role must be ('студент', 'аспирант', 'сотрудник')")
  

def adviser_validate(val: str):
    if val:
        pattern = re.compile(r"^(?:[А-Я]|[а-я]|-|.)+$")
        if pattern.match(val):
            return val
        else:
            raise ValueError("Adviser name must contain only russian letters and '-', '.'")


def coauthors_validate(val: Coauthors):
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
    if val:
        try:
            datetime.fromisoformat(val)
            return val
        except ValueError:
            raise ValueError("date must be represented in ISO 8601 form")
    else:
        return datetime.now().astimezone().isoformat()


def updated_timemark(val: str):
    return datetime.now().astimezone().isoformat()

