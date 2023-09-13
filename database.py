import random

conferences_json = [
    {
        "conference_id": "1",
        "google_sheet_id": "first",
        "conference_name_russian": "76-я международная студенческая научная конференция ГУАП",
        "conference_short_name_russian": "МСНК 2023",
        "conference_name_english": "",
        "conference_short_name_english": "",
        "organizing_organization": "ГУАП",
        "registration_start_date": "01-08-2023",
        "registration_end_date": "01-09-2023",
        "submission_start_date": "01-08-2023",
        "submission_end_date": "01-09-2023",
        "conference_start_date": "04-09-2023",
        "conference_end_date": "09-09-2023",
        "conference_website_url": "",
        "contact_email": "example@example.com"
    },
    {
        "conference_id": "2",
        "google_sheet_id": "second",
        "conference_name_russian": "Аэрокосмическое приборостроение и эксплуатационные технологии",
        "conference_short_name_russian": "АПиЭТ 2023",
        "conference_name_english": "",
        "conference_short_name_english": "",
        "organizing_organization": "Московский авиационный институт",
        "registration_start_date": "24-07-2023",
        "registration_end_date": "30-07-2023",
        "submission_start_date": "20-07-2023",
        "submission_end_date": "27-07-2023",
        "conference_start_date": "01-08-2023",
        "conference_end_date": "03-08-2023",
        "conference_website_url": "",
        "contact_email": "example@example.com"
    },
    {
        "conference_id": "3",
        "google_sheet_id": "third",
        "conference_name_russian": "Волновая электроника и инфокоммуникационные системы",
        "conference_short_name_russian": "ВолЭлИнфоСистемы",
        "conference_name_english": "",
        "conference_short_name_english": "",
        "organizing_organization": "Гуап",
        "registration_start_date": "02-09-2023",
        "registration_end_date": "14-09-2023",
        "submission_start_date": "02-09-2023",
        "submission_end_date": "14-09-2023",
        "conference_start_date": "15-09-2023",
        "conference_end_date": "18-09-2023",
        "conference_website_url": "",
        "contact_email": "example@example.com"
    }
]

application_json = [
    {
        "id": "1",
        "conference_id": "1",
        "telegram_id": "",
        "discord_id": "1234",
        "submitted_at": "2023-07-15T13:23:53.697941+03:00",
        "updated_at": "2023-07-15T13:23:53.697941+03:00",
        "email": "example@example.com",
        "phone": "+79001234567",
        "name": "Иван",
        "surname": "Иванов",
        "patronymic": "Иванович",
        "university": "ГУАП",
        "student_group": "4032",
        "applicant_role": "студент",
        "title": "Заявка раз",
        "adviser": "проф. Сидоров А.В.",
        "coauthors": [
            {"name": "Петр", "surname": "Петров", "patronymic": "Петрович"},
            {"name": "Ноунейм", "surname": "Аноним", "patronymic": "Ноунеймович"}
        ]
    },
    {
        "id": "2",
        "conference_id": "1",
        "telegram_id": "",
        "discord_id": "1234",
        "submitted_at": "2023-07-15T13:23:53.697941+03:00",
        "updated_at": "2023-07-15T13:23:53.697941+03:00",
        "email": "example@example.com",
        "phone": "+79001234567",
        "name": "Иван",
        "surname": "Иванов",
        "patronymic": "Иванович",
        "university": "ГУАП",
        "student_group": "4032",
        "applicant_role": "студент",
        "title": "Заявка два",
        "adviser": "проф. Васильев А.В.",
        "coauthors": [
            {"name": "Анатолий", "surname": "Толянов", "patronymic": "Тольевич"},
            {"name": "Ноунейм", "surname": "Аноним", "patronymic": "Ноунеймович"},
            {"name": "Петр", "surname": "Петров", "patronymic": "Петрович"}
        ]
    },
    {
        "id": "3",
        "conference_id": "2",
        "telegram_id": "",
        "discord_id": "1234",
        "submitted_at": "2023-07-15T13:23:53.697941+03:00",
        "updated_at": "2023-07-15T13:23:53.697941+03:00",
        "email": "example@example.com",
        "phone": "+79001234567",
        "name": "Иван",
        "surname": "Иванов",
        "patronymic": "Иванович",
        "university": "ГУАП",
        "student_group": "4032",
        "applicant_role": "студент",
        "title": "Заявка три",
        "adviser": "проф. Сидоров А.В.",
        "coauthors": [
            {"name": "Александр", "surname": "Александров", "patronymic": "Александрович"},
            {"name": "Анатолий", "surname": "Толянов", "patronymic": "Тольевич"}
        ]
    }
]


publications_json = [
    {
        "id": "1",  # идентификатор публикации совпадает с идентификатором заявки, к которой данная публикация привязана
        "publication_title": "Название публикации",  # может отличаться от названия доклада в исходной заявке
        "upload_date": "2023-07-15T13:23:53.697941+03:00",
        "review_status": "in progress",  # одно из значений "in progress", "changes requested", "rejected", "accepted"
        "download_url": "URL для скачивания",
        "keywords": "список; ключевых; слов; через; точу с запятой",
        "abstract": "аннотация к статье"
    }

]


def create_new_application(id, conf_id, discord_id, date):
    new_application = {
        "id": id,
        "conference_id": conf_id,
        "telegram_id": " ",
        "discord_id": discord_id,
        "submitted_at": date,
        "updated_at": " ",
        "email": " ",
        "phone": " ",
        "name": " ",
        "surname": " ",
        "patronymic": " ",
        "university": " ",
        "student_group": " ",
        "applicant_role": " ",
        "title": "Новая заявка",
        "adviser": " ",
        "coauthors": []
    }
    return new_application


def get_unique_id(existing_applications=application_json):
    existing_ids = [int(app["id"]) for app in existing_applications]
    new_id = random.randint(1, 1000)
    while new_id in existing_ids:
        new_id = random.randint(1, 1000)
    return str(new_id)


def create_new_publication(id, upload_date):
    new_publication = {
        "id": id,  # идентификатор публикации совпадает с идентификатором заявки, к которой данная публикация привязана
        "publication_title": " ",  # может отличаться от названия доклада в исходной заявке
        "upload_date": upload_date,
        "review_status": "in progress",  # одно из значений "in progress", "changes requested", "rejected", "accepted"
        "download_url": "",
        "keywords": "",
        "abstract": ""
    }
    return new_publication



