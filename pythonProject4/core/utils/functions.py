import datetime

from core.data.test_data import application_json, publications_json


def get_conference_view(conf) -> str:
    return f"""
        Название: {conf["name_rus"]}
        Аббревиатура: {conf["name_rus_short"]}
        Name: {conf["name_eng"]}
        Short name: {conf["name_eng_short"]}
        Дата начала регистрации: {conf["registration_start_date"]}
        Дата конца регистрации: {conf["registration_end_date"]}
        Дата начала приема докладов: {conf["submission_start_date"]}
        Дата конца приема статей: {conf["submission_end_date"]}
        Дата начала конференции: {conf["conf_start_date"]}
        Дата конца конференции: {conf["conf_end_date"]}
        Организатор: {conf["organized_by"]}
        url: {conf["url"]}
        email: {conf["email"]}
    """


def get_conference_status(conf):
    registration_start_date = datetime.datetime.strptime(conf['registration_start_date'], "%d.%m.%Y").date()
    registration_end_date = datetime.datetime.strptime(conf['registration_end_date'], "%d.%m.%Y").date()
    current_date = datetime.datetime.now().date()

    if current_date < registration_start_date:
        return "Появится"
    elif registration_start_date <= current_date <= registration_end_date:
        return "Доступна"
    elif current_date > registration_end_date:
        return "Закончена"


def applications(conf_id, telegram_id):
    return [x for x in application_json if x["conf_id"] == conf_id and x["telegram_id"] == str(telegram_id)]


def findPublicationIndex(app_id):
    return next((index for index, pub in enumerate(publications_json) if pub['id'] == app_id), None)


def get_last_id(items):  # возвращает следующий за максимальным id в applications_json
    if items:
        max = items[0]['id']
        for item in items:
            if max < item['id']:
                max = item['id']

        return max + 1
    else:
        return 1
