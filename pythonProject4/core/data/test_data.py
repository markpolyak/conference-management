import random

conferences_json = [
    {
        "id": 1,  # conference_id
        "name_rus": "76-я международная студенческая научная конференция ГУАП",
        "name_rus_short": "МСНК-2023",
        "name_eng": "",
        "name_eng_short": "",
        "registration_start_date": "20.02.2023",  # дата начала приема заявок
        "registration_end_date": "14.04.2024",  # дата окончания приема заявок
        "submission_start_date": "01.05.2024",  # дата начала приема докладов для публикации
        "submission_end_date": "30.05.2023",  # дата окончания приема докладов
        "conf_start_date": "17.04.2023",  # дата начала конференции
        "conf_end_date": "21.04.2024",  # дата окончания конференции
        "organized_by": "ГУАП",  # название организации, проводящей мероприятие
        "url": "https://guap.ru/msnk/",
        "email": "example@example.com"
    },
    {
        "id": 2,  # conference_id
        "name_rus": "ФБВГ",
        "name_rus_short": "ФБВГ-2023",
        "name_eng": "",
        "name_eng_short": "",
        "registration_start_date": "20.02.2022",  # дата начала приема заявок
        "registration_end_date": "14.04.2022",  # дата окончания приема заявок
        "submission_start_date": "01.05.2023",  # дата начала приема докладов для публикации
        "submission_end_date": "30.05.2023",  # дата окончания приема докладов
        "conf_start_date": "17.04.2023",  # дата начала конференции
        "conf_end_date": "21.04.2023",  # дата окончания конференции
        "organized_by": "ГУАП",  # название организации, проводящей мероприятие
        "url": "https://guap.ru/msnk/",
        "email": "example@example.com"
    },
    {
        "id": 3,  # conference_id
        "name_rus": "76-я международная студенческая научная конференция ГУАП",
        "name_rus_short": "МСНК-2023",
        "name_eng": "",
        "name_eng_short": "",
        "registration_start_date": "20.02.2030",  # дата начала приема заявок
        "registration_end_date": "14.04.2031",  # дата окончания приема заявок
        "submission_start_date": "01.05.2024",  # дата начала приема докладов для публикации
        "submission_end_date": "30.05.2023",  # дата окончания приема докладов
        "conf_start_date": "17.04.2023",  # дата начала конференции
        "conf_end_date": "21.04.2024",  # дата окончания конференции
        "organized_by": "ГУАП",  # название организации, проводящей мероприятие
        "url": "https://guap.ru/msnk/",
        "email": "example@example.com"
    },
]

application_json = [
    {
        "id": 1,
        "conf_id": 1,
        "telegram_id": "1708426303",
        "discord_id": "4321",
        "submitted_at": "2023-07-15T13:23:53.697941+03:00",
        "updated_at": "2023-07-15T13:23:53.697941+03:00",
        "email": "example@example.com",
        "phone": "+79001234567",
        "name": "Иван",
        "surname": "Иванов",
        "patronymic": "Иванович",
        "university": "ГУАП",
        "student_group": "4031",
        "applicant_role": "студент",
        "title": "работа 1",
        "adviser": "проф. Сидоров А.В.",
        "coauthors": [
            {"name": "Петр", "surname": "Петров", "patronymic": "Петрович"},
            {"name": "Ноунейм", "surname": "Аноним", "patronymic": "Ноунеймович"}
        ]
    },
    {
        "id": 2,
        "conf_id": 1,
        "telegram_id": "989233922",
        "discord_id": "4321",
        "submitted_at": "2023-07-15T13:23:53.697941+03:00",
        "updated_at": "2023-07-15T13:23:53.697941+03:00",
        "email": "example@example.com",
        "phone": "+79001234567",
        "name": "Иван",
        "surname": "Иванов",
        "patronymic": "Иванович",
        "university": "ГУАП",
        "student_group": "4031",
        "applicant_role": "студент",
        "title": "Название работы, подаваемой на конференцию",
        "adviser": "проф. Сидоров А.В.",
        "coauthors": [
            {"name": "Петр", "surname": "Петров", "patronymic": "Петрович"},
            {"name": "Ноунейм", "surname": "Аноним", "patronymic": "Ноунеймович"}
        ]
    },
    {
        "id": 3,
        "conf_id": 2,
        "telegram_id": "989233922",
        "discord_id": "4321",
        "submitted_at": "2023-07-15T13:23:53.697941+03:00",
        "updated_at": "2023-07-15T13:23:53.697941+03:00",
        "email": "example@example.com",
        "phone": "+79001234567",
        "name": "Иван",
        "surname": "Иванов",
        "patronymic": "Иванович",
        "university": "ГУАП",
        "student_group": "4031",
        "applicant_role": "студент",
        "title": "работа 2",
        "adviser": "проф. Сидоров А.В.",
        "coauthors": [
            {"name": "Петр", "surname": "Петров", "patronymic": "Петрович"},
            {"name": "Ноунейм", "surname": "Аноним", "patronymic": "Ноунеймович"}
        ]
    },

]

publications_json = [
    {
        "id": 1,  # идентификатор публикации совпадает с идентификатором заявки, к которой данная публикация привязана
        "publication_title": "Название публикации",  # может отличаться от названия доклада в исходной заявке
        "upload_date": "2023-07-15T13:23:53.697941+03:00",
        "review_status": "in progress",  # одно из значений "in progress", "changes requested", "rejected", "accepted"
        "download_url": "URL для скачивания",
        "keywords": "список; ключевых; слов; через; точу с запятой",
        "abstract": "аннотация к статье"
    }

]

authors_json = [
    {
        "id": 1,  # идентификатор автора в общем списке всех авторов, зарегистрированных на конференции
        "application_id": 1,  # идентификатор заявки на участие в конференции
        "name": "Имя автора",
        "surname": "Фамилия автора",
        "patronymic": "Отчество автора (при наличии)",
        "email": "example@example.com",
        "phone": "+79876543210",
        "bio": "биография автора",
        "organization": "Санкт-Петербургский государственный университет аэрокосмического приборостроения",
        "role": "Старшний научный сотрудник"
    }
]


