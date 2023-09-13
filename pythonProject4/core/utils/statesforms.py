from aiogram.fsm.state import StatesGroup, State


class AppInput(StatesGroup):
    waiting_for_name = State()  # Ожидание имени
    waiting_for_surname = State()  # Ожидание фамилии
    waiting_for_patronymic = State()  # Ожидание отчества
    waiting_for_university = State()  # Ожидание университета
    waiting_for_student_group = State()  # Ожидание группы студента
    waiting_for_applicant_role = State()  # Ожидание роли заявителя
    waiting_for_title = State()  # Ожидание названия работы
    waiting_for_adviser = State()
    waiting_for_discord_id = State()
    waiting_for_email = State()
    waiting_for_phone = State()
    waiting_for_coauthors = State()


class PublicationInput(StatesGroup):
    waiting_for_file = State()
    waiting_for_confirmation = State()
    waiting_for_data = State()


class AuthorInput(StatesGroup):
    publication_view = State()
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_patronymic = State()
    waiting_for_email = State()
    waiting_for_phone = State()
    waiting_for_bio = State()
    waiting_for_organization = State()
    waiting_for_role = State()



