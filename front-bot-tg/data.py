import random
from fastapi import FastAPI, HTTPException, Depends, Request


start_message = """Привет!

Добро пожаловать в нашу систему, которая предоставляет возможность подать заявку на интересующую тебя конференцию, а также редактировать заявку по необходимости. Мы хотим, чтобы ты чувствовал себя комфортно при работе с нами, поэтому хотим прозрачно обсудить передачу данных.

При использовании нашей системы, пожалуйста, учти, что мы можем передавать твои данные третьим лицам в определенных случаях, связанных с организацией конференции. Это может включать, например, передачу информации о заявке организаторам мероприятия или связанным структурам. Мы гарантируем, что передача данных будет осуществляться в соответствии с применимыми законами о защите данных и только для целей, связанных с конференцией.

Твоя приватность очень важна для нас, и мы обеспечиваем безопасность и конфиденциальность твоих данных. Если у тебя есть вопросы или требуется дополнительная информация о передаче данных, не стесняйся обращаться к нам.

Благодарим тебя за выбор нашей системы для подачи заявок на конференции. Мы ценим твою доверие и готовы помочь тебе в любое время."""

conferences_json_web = [
{
  "id": 1, # conference_id
  "name_rus": "76-я международная студенческая научная конференция ГУАП",
  "name_rus_short": "МСНК-2023",
  "name_eng": "",
  "name_eng_short": "",
  "registration_start_date": "20.02.2023", # дата начала приема заявок
  "registration_end_date": "14.04.2024", # дата окончания приема заявок
  "submission_start_date": "01.05.2024", # дата начала приема докладов для публикации
  "submission_end_date": "30.05.2023", # дата окончания приема докладов
  "conf_start_date": "17.04.2023", # дата начала конференции
  "conf_end_date": "21.04.2024", # дата окончания конференции
  "organized_by": "ГУАП", # название организации, проводящей мероприятие
  "url": "https://guap.ru/msnk/",
  "email": "example@example.com"
},
{
  "id": 2, # conference_id
  "name_rus": "ФБВГ",
  "name_rus_short": "ФБВГ-2023",
  "name_eng": "",
  "name_eng_short": "",
  "registration_start_date": "20.02.2022", # дата начала приема заявок
  "registration_end_date": "14.04.2022", # дата окончания приема заявок
  "submission_start_date": "01.05.2023", # дата начала приема докладов для публикации
  "submission_end_date": "30.05.2023", # дата окончания приема докладов
  "conf_start_date": "17.04.2023", # дата начала конференции
  "conf_end_date": "21.04.2023", # дата окончания конференции
  "organized_by": "ГУАП", # название организации, проводящей мероприятие
  "url": "https://guap.ru/msnk/",
  "email": "example@example.com"
}
]

application_json_web_approval = [
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
} ,
{
  "id": 2,
  "conf_id": 1,
  "telegram_id": "123",
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
} ,
{
  "id": 3,
  "conf_id": 2,
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
  "title": "работа 2", 
  "adviser": "проф. Сидоров А.В.", 
  "coauthors": [
    {"name": "Петр", "surname": "Петров", "patronymic": "Петрович"}, 
    {"name": "Ноунейм", "surname": "Аноним", "patronymic": "Ноунеймович"}
  ]
} 
]

publication_json_web = [
{
  "id": 1, # идентификатор публикации совпадает с идентификатором заявки, к которой данная публикация привязана
  "publication_title": "Название публикации", # может отличаться от названия доклада в исходной заявке
  "upload_date": "2023-07-15T13:23:53.697941+03:00", 
  "review_status": "in progress", # одно из значений "in progress", "changes requested", "rejected", "accepted"
  "download_url": "URL для скачивания",
  "keywords": "список; ключевых; слов; через; точу с запятой",
  "abstract": "аннотация к статье"
}
    
]

application_json_web =[]

def create_new_application(id,conf_id,telegram_id,date, existing_applications = application_json_web_approval):
    new_application = {
        "id": id,
        "conf_id": conf_id,
        "telegram_id": telegram_id,
        "discord_id": "",
        "submitted_at": date,
        "updated_at": "",
        "email": "",
        "phone": "",
        "name": "",
        "surname": "",
        "patronymic": "",
        "university": "",
        "student_group": "",
        "applicant_role": "",
        "title": "Новая заявка",
        "adviser": "",
        "coauthors": []
    }
    return new_application

def get_unique_id(existing_applications = application_json_web):
    existing_ids = [app["id"] for app in existing_applications]
    new_id = random.randint(1, 1000)
    while new_id in existing_ids:
        new_id = random.randint(1, 1000)
    return new_id

def create_new_publication(id,upload_date):
    new_publication =  {
  "id": id, # идентификатор публикации совпадает с идентификатором заявки, к которой данная публикация привязана
  "publication_title": " ", # может отличаться от названия доклада в исходной заявке
  "upload_date":  upload_date,
  "review_status": "in progress", # одно из значений "in progress", "changes requested", "rejected", "accepted"
  "download_url": "",
  "keywords": "",
  "abstract": ""
}
    return new_publication
        
change_application_dict = {
  "discord_id": "Дискорд", 
  "email": "email", 
  "phone": "Номер телефона", 
  "name": "Имя", 
  "surname": "Фамилия", 
  "patronymic": "Отчество", 
  "university": "Университет", 
  "student_group": "Группа", 
  "applicant_role": "Должность", 
  "title": "Название работы", 
  "adviser": "Научный руководитель", 
  "coauthors": "Соавторы",
  "publication_title": "Название публикации",
  "download_url": "URL для скачивания",
"keywords": "список ключевых слов через точу с запятой",
"abstract": "аннотация к статье"

}

json_to_name = lambda x: change_application_dict[x]

application_json_web = [{
        "id": 0,
        "conf_id": 0,
        "telegram_id": "0",
        "discord_id": "",
        "submitted_at": "",
        "updated_at": "",
        "email": "",
        "phone": "",
        "name": "",
        "surname": "",
        "patronymic": "",
        "university": "",
        "student_group": "",
        "applicant_role": "",
        "title": "Новая заявка",
        "adviser": "",
        "coauthors": []
    }]

app = FastAPI()

@app.get("/conferences")
def get_conferences():
    if conferences_json_web:
        return {"conferences_json": conferences_json_web}
    else:
        raise HTTPException(status_code=404, detail="not found")
  
@app.get("/application")
def get_application():
    if application_json_web:
        return {"application_json": application_json_web}
    else:
        raise HTTPException(status_code=404, detail="not found")

@app.post("/new_application/")
async def edit_application(request: Request): 
    application = await request.json()

    id = application["id"]

    for x in application_json_web:
        if x["id"] == id:
            application_json_web.remove(x)
            
    application_json_web.append(application)

    return ({"message": "Application successfully updated"}), 200

@app.get("/publication")
def get_application():
    if publication_json_web:
        return {"publication_json": publication_json_web}
    else:
        raise HTTPException(status_code=404, detail="not found")
    
@app.post("/new_publication/")
async def edit_application(request: Request): 
    publication = await request.json()

    id = publication["id"]

    for x in publication_json_web:
        if x["id"] == id:
            publication_json_web.remove(x)
            
    publication_json_web.append(publication)

    return ({"message": "Publication successfully updated"}), 200

@app.get("/application_approval")
def get_application():
    if application_json_web_approval:
        return {"application_approval": application_json_web_approval}
    else:
        raise HTTPException(status_code=404, detail="not found")

@app.post("/new_approval_application/")
async def edit_application(request: Request): 
    publication = await request.json()

    id = publication["id"]

    for x in application_json_web_approval:
        if x["id"] == id:
            application_json_web_approval.remove(x)
            
    application_json_web_approval.append(publication)

    return ({"message": "Publication successfully updated"}), 200



    # Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)