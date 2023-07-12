import pytest
from pydantic import ValidationError

from src.schema import Application, ApplicationCreate


def test_application_create():
    """
    Функция для тестирования схемы ApplicationCreate
    """

    app_data = {
        "telegram_id": "1234",
        "discord_id": "4321",
        "email": "test@test.com",
        "phone": "+79217701199",
        "name": "Test",
        "surname": "Tester",
        "patronymic": "TestTest",
        "university": "SUAI",
        "student_group": "4031",
        "title": "Testing app schema",
        "adviser": "Durdma",
        "coauthors": [{"name": "coath_one", "surname": "coath_surname_one",
                        "patronymic": "coath_patr_one"}]
    }

    app_examp = ApplicationCreate(**app_data)

    assert app_examp.telegram_id == "1234"
    assert app_examp.discord_id == "4321"
    assert app_examp.email == "test@test.com"

    # trim "tel:", its str
    assert app_examp.phone == "tel:+7-921-770-11-99"
    assert app_examp.name == "Test"
    assert app_examp.surname == "Tester"
    assert app_examp.patronymic == "TestTest"
    assert app_examp.university == "SUAI"
    assert app_examp.student_group == "4031"
    assert app_examp.title == "Testing app schema"
    assert app_examp.adviser == "Durdma"
    assert app_examp.coauthors == [{"name": "coath_one", "surname": "coath_surname_one",
                        "patronymic": "coath_patr_one"}]
    app_examp.trim_phone()
    assert app_examp.phone == "+7-921-770-11-99"


def test_application_schema():
    """
    Функция для тестирования схемы Application
    """
    app_data = {
        "id": 1,
        "telegram_id": "1234",
        "discord_id": "4321",
        "email": "test@test.com",
        "phone": "+79217701199",
        "name": "Test",
        "surname": "Tester",
        "patronymic": "TestTest",
        "university": "SUAI",
        "student_group": "4031",
        "title": "Testing app schema",
        "adviser": "Durdma",
        "coauthors": [{"name": "coath_one", "surname": "coath_surname_one",
                        "patronymic": "coath_patr_one"}]
    }

    app_examp = Application(**app_data)

    assert app_examp.id == 1
    assert app_examp.telegram_id == "1234"
    assert app_examp.discord_id == "4321"
    assert app_examp.email == "test@test.com"
    assert app_examp.phone == "tel:+7-921-770-11-99"
    assert app_examp.name == "Test"
    assert app_examp.surname == "Tester"
    assert app_examp.patronymic == "TestTest"
    assert app_examp.university == "SUAI"
    assert app_examp.student_group == "4031"
    assert app_examp.title == "Testing app schema"
    assert app_examp.adviser == "Durdma"
    assert app_examp.coauthors == [{"name": "coath_one", "surname": "coath_surname_one",
                        "patronymic": "coath_patr_one"}]
    