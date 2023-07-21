from fastapi import FastAPI, HTTPException, Query, Header
from pydantic import BaseModel
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime
import uvicorn
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    


GOOGLE_SHEET_ID = os.getenv("TOKEN")

# Модель данных для конференции
class Conference(BaseModel):
    id: int =  None
    name_rus: str
    name_rus_short: str
    name_eng: str = None
    name_eng_short: str = None
    registration_start_date: str
    registration_end_date: str
    submission_start_date: str
    submission_end_date: str
    conf_start_date: str
    conf_end_date: str
    organized_by: str
    url: str = None
    email: str


# Модель данных для конференции
class ConferenceUpdate(BaseModel):
    id: int  = None
    name_rus: str = None
    name_rus_short: str = None
    name_eng: str = None
    name_eng_short: str = None
    registration_start_date: str = None
    registration_end_date: str = None
    submission_start_date: str = None
    submission_end_date: str = None
    conf_start_date: str = None
    conf_end_date: str = None
    organized_by: str = None
    url: str = None
    email: str = None

app = FastAPI()

path = os.path.abspath(os.path.dirname(__file__)) + '\credentials.json'

# Загрузка учетных данных и авторизация в Google Sheets API
with open(path) as f:
    creds_data = json.load(f)

credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, ['https://www.googleapis.com/auth/spreadsheets'])
client = gspread.authorize(credentials)


# Получение экземпляра таблицы
sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

# Функция для проверки валидности токена
def is_valid_token(token: str) -> bool:
    token_sheet = os.getenv("TOKEN")
    
    if token == token_sheet:
        return True
    else:
        return False


# Функция для получения номера последней строки в таблице
def get_last_row_number():
    try:
        values = sheet.col_values(1)
        return len(values)
    except gspread.exceptions.APIError as e:
        print("Ошибка при получении данных из Google Sheets:", e)
        return None

# Обработчик корневого пути
@app.get("/")
def read_root():
    return {"Hello": "World"}


# Получение списка конференций
@app.get('/conferences')
def get_conferences(filter: str = Query("active", enum=["all", "active", "past", "future"])):
    if filter not in ["all", "active", "past", "future"]:
        raise HTTPException(status_code=400, detail="Invalid filter value. Allowed values: 'all', 'active', 'past', 'future'.")

    # Чтение данных из таблицы Google Sheets
    data = sheet.get_all_records()
    today = datetime.now()
    formatted_date_str = today.strftime("%d.%m.%Y")
    formatted_date = datetime.strptime(formatted_date_str, "%d.%m.%Y").date()
    
    # Фильтрация данных в соответствии с параметром filter
    if filter == "active":
        filtered_data = [record for record in data if datetime.strptime(record["registration_start_date"],"%d.%m.%Y").date() \
            <= formatted_date <= datetime.strptime(record["registration_end_date"],"%d.%m.%Y").date()]
    elif filter == "past":
        filtered_data = [record for record in data if datetime.strptime(record["registration_end_date"],"%d.%m.%Y").date() < formatted_date]
    elif filter == "future":
        filtered_data = [record for record in data if datetime.strptime(record["registration_start_date"],"%d.%m.%Y").date() > formatted_date]
    else:
        filtered_data = data

    result = [
        {
            "id": record["id"],
            "name_rus_short": record["name_rus_short"],
            "name_eng_short": record["name_eng_short"],
            "conf_start_date": record["conf_start_date"],
            "conf_end_date": record["conf_end_date"]
        }
        for record in filtered_data
    ]

    return result


# Эндпоинт для получения информации о конференции по ее ID
@app.get('/conferences/{conference_id}')
def get_conference(conference_id: int, authorization: str = Header(None)):
    try:
        # Чтение данных из таблицы Google Sheets
        data = sheet.get_all_records()

        # Поиск конференции по значению поля "id"
        conference = next((record for record in data if record["id"] == conference_id), None)

        if conference is None:
            raise HTTPException(status_code=404, detail='Конференция не найдена')

        conference = Conference(**conference)

        if authorization and is_valid_token(authorization.replace("Bearer ", "")):
            # Включаем поле "google_spreadsheet" в ответе
            conference_dict = conference.dict()
            conference_dict["google_spreadsheet"] = GOOGLE_SHEET_ID
            return conference_dict
    
        raise HTTPException(status_code=403, detail='Неверный токен авторизации')
    
    except IndexError:
        raise HTTPException(status_code=404, detail='Конференция не найдена')


# Добавление новой заявки на участие в конференции
@app.post('/conferences')
def create_conference(conference: Conference, authorization: str = Header(None)):
    # Проверка наличия валидного токена авторизации
    if not authorization or not is_valid_token(authorization.replace("Bearer ", "")):
        raise HTTPException(status_code=403, detail='Неверный токен авторизации')

    # Чтение данных из таблицы Google Sheets
    data = sheet.get_all_records()

    # Получение максимального значения id из существующих записей
    max_id = max([int(record["id"]) for record in data]) if data else 0

    # Генерируем новый id, увеличивая его на 1 относительно максимального значения
    conference_id = str(max_id + 1)

    # Добавление данных в таблицу Google Sheets
    row_data = conference.dict()

    # Вставляем сгенерированное id в данные перед добавлением в таблицу
    row_data["id"] = conference_id

    # Вставляем данные в таблицу Google Sheets
    last_row_number = get_last_row_number()
    if last_row_number is not None:
        row_values = list(row_data.values())
        sheet.insert_row(row_values, index=last_row_number + 1)

    # Возвращаем JSON с добавленной информацией и id
    response_data = row_data
    response_data["google_spreadsheet"] = GOOGLE_SHEET_ID
    return response_data


# Редактирование конференции по идентификатору
@app.put('/conferences/{conference_id}')
def update_conference(conference_id: int, conference_data: ConferenceUpdate, authorization: str = Header(None)):
    
    
    # Проверка наличия валидного токена авторизации
    if not authorization or not is_valid_token(authorization.replace("Bearer ", "")):
        raise HTTPException(status_code=403, detail='Неверный токен авторизации')

    # Получение текущих данных о конференции из Google Sheets
    try:
        record = sheet.find(str(conference_id))
    except gspread.exceptions.CellNotFound:
        raise HTTPException(status_code=404, detail='Конференция с указанным id не найдена')

    row = sheet.row_values(record.row)
    
    # Создание объекта Conference с текущими данными о конференции
    current_conference = ConferenceUpdate(**dict(zip(ConferenceUpdate.__fields__.keys(), row)))

    # Обновление полей в текущем объекте Conference значениями из запроса, если они указаны
    for field, value in conference_data.dict(exclude_unset=True).items():
        setattr(current_conference, field, value)

    array  = list(current_conference.dict().values())

    new_array = []
    new_array.append(array)
 
    # Обновление данных в таблице Google Sheets
    sheet.update('A'+str(record.row)+':N'+str(record.row), new_array)

    # Возвращаем JSON с обновленной информацией о конференции
    response_data = current_conference.dict()
    response_data["google_spreadsheet"] = GOOGLE_SHEET_ID
    response_data["id"] = conference_id
    return response_data


if __name__ == "__main__":
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
