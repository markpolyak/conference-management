from copy import deepcopy
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
# from typing import List
from datetime import datetime
import gspread

from .schemas import UserSchema, UpdateUserSchema
from .services import get_worksheet, append_to_worksheet

router = APIRouter()




@router.post("/{conference_id}/applications/")
async def create_users(conference_id: int, user: UserSchema):
    # Вызов функции table_definition и сохранение результата
    table_result = table_definition(conference_id)
    if "error_response" in table_result:
        return JSONResponse(
            status_code=table_result["status_code"],
            content={"data": table_result["error_response"]}
        )
    # Извлечение значения new_identifier из результата
    new_identifier = table_result["new_identifier"]
    worksheet = get_worksheet(new_identifier)
    current_time = datetime.now().astimezone().isoformat()
    next_user_id = len(worksheet.get_all_values()) + 1
    row_values = [
        next_user_id,
        user.telegram_id,
        user.discord_id,
        user.email,
        user.phone,
        user.name,
        user.surname,
        user.patronymic,
        user.university,
        user.student_group,
        user.title,
        user.adviser,
        user.applicant_role,
        current_time,
        current_time,
        ', '.join(f'{c.name} {c.surname} {c.patronymic}' for c in user.coauthors) if user.coauthors else None
    ]
    append_to_worksheet(row_values, worksheet, worksheet=worksheet)

    data = []
    # Создаем объект user_data с вашим значением submitted_at
    user_data = {
        "id": next_user_id,
        "telegram_id": user.telegram_id,
        "discord_id": user.discord_id,
        "email": user.email,
        "phone": user.phone,
        "name": user.name,
        "surname": user.surname,
        "patronymic": user.patronymic,
        "university": user.university,
        "student_group": user.student_group,
        "title": user.title,
        "adviser": user.adviser,
        "applicant_role": user.applicant_role,
        "submitted_at": current_time,
        "updated_at": current_time,
        "coauthors": ', '.join(
            f'{c.name} {c.surname} {c.patronymic}' for c in user.coauthors) if user.coauthors else None
    }
    data.append(user_data)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"data": data}
    )


def table_definition(conference_id: int):
    new_identifier = "1PT-q0EvdZ21P7MN598qtE0cuWyleMSX0aGieuahmyH4"
    deadline_time = "2002-08-27T08:00:00+03:00"
    worksheet = get_worksheet(new_identifier)
    get_all_values = worksheet.get_all_values()
    # get_all_values_index = get_all_values[conference_id - 1]
    var = len(get_all_values)

    identifier = 3
    deadline = 2

    identif_updated = True
    if var >= conference_id > 1:
        identif_updated = False
        new_identifier =  get_all_values[conference_id - 1][identifier]
        deadline_time =  get_all_values[conference_id - 1][deadline]

    current_time = datetime.now().astimezone().isoformat()
    # Преобразуем строки в объекты datetime
    deadline_time_dt = datetime.fromisoformat(deadline_time)
    current_time_dt = datetime.fromisoformat(current_time)

    if identif_updated:
        return {"error_response": "Conference not found", "status_code": status.HTTP_404_NOT_FOUND}
    elif deadline_time_dt < current_time_dt:
        return {"error_response": "Time is up", "status_code": status.HTTP_403_FORBIDDEN}

        # Возврат значения new_identifier
    return {"new_identifier": new_identifier}


@router.patch("/{conference_id}/applications/{application_id}")
def update_user(conference_id: int, application_id: int, user: UpdateUserSchema):
    table_result = table_definition(conference_id)
    if "error_response" in table_result:
        return JSONResponse(
            status_code=table_result["status_code"],
            content={"data": table_result["error_response"]}
        )
    # Извлечение значения new_identifier из результата
    new_identifier = table_result["new_identifier"]
    worksheet = get_worksheet(new_identifier)
    get_all_values = worksheet.get_all_values()

    # new_identifier = "1PT-q0EvdZ21P7MN598qtE0cuWyleMSX0aGieuahmyH4"
    updated_at = datetime.now().astimezone().isoformat()

    # worksheet = get_worksheet(new_identifier)
    var2 = len(get_all_values)
    user_as_dict_telegram = user.telegram_id
    user_as_dict_discord = user.discord_id

    if application_id > var2 or application_id < 2:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "User not exist"}
        )
    # list_of_dicts = worksheet.get_all_records()
    # print(list_of_dicts[4]["telegram_id"])
    data = user.model_dump()
    print(data)
    print("----------------")

    index = application_id - 1
    get_all_values_index = get_all_values[index]

    telega_id = 1
    dis_id = 2
    submitted = 13

    submitted_at = get_all_values_index[submitted]

    telegram_id = get_all_values_index[telega_id]

    discord_id = get_all_values_index[dis_id]

    coauthors_list = []
    if data.get('coauthors'):
        coauthors_list = [f"{coauthor['name']} {coauthor['surname']} {coauthor['patronymic']}" for coauthor in
                          data['coauthors'] if coauthor is not None]

    result_list = [
        application_id,
        telegram_id,
        discord_id,
        data["email"],
        data["phone"],
        data["name"],
        data["surname"],
        data["patronymic"],
        data["university"],
        data["student_group"],
        data["title"],
        data["adviser"],
        data["applicant_role"],
        submitted_at,
        updated_at,
        ", ".join(coauthors_list)
    ]
    # here
    user_updated = False
    # worksheet.update_cell(application_id, 1, '19191919')

    print("@@@")
    print(telegram_id)
    print(discord_id)
    if telegram_id == user_as_dict_telegram:
        print("telega")
        for i in range(len(result_list)):
            if result_list[i] is not None and user_as_dict_telegram.strip():
                user_updated = True
                worksheet.update_cell(application_id, i + 1, result_list[i])
                print(worksheet.update_cell(application_id, i + 1, result_list[i]))

    elif discord_id == user_as_dict_discord:
        print("dis")
        for i in range(len(result_list)):
            if result_list[i] is not None and user_as_dict_discord.strip():
                user_updated = True
                worksheet.update_cell(application_id, i + 1, result_list[i])
                print(worksheet.update_cell(application_id, i + 1, result_list[i]))

    if user_updated:
        get_all_values = worksheet.get_all_values()
        get_all_values_index = get_all_values[index]
        information = []
        output_data = {
            "id": str(application_id),
            "telegram_id": telegram_id,
            "discord_id": discord_id,
            "email": get_all_values_index[3],
            "phone": get_all_values_index[4],
            "name": get_all_values_index[5],
            "surname": get_all_values_index[6],
            "patronymic": get_all_values_index[7],
            "university": get_all_values_index[8],
            "student_group": get_all_values_index[9],
            "title": get_all_values_index[10],
            "adviser": get_all_values_index[11],
            "applicant_role": get_all_values_index[12],
            "submitted_at": submitted_at,
            "updated_at": get_all_values_index[14],
            "coauthors": get_all_values_index[15]
        }
        information.append(output_data)
        print('updated')
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"data": information}
        )
    else:
        # В случае, если не было выполнено условие в цикле
        print('not updated')
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": "User not verified"}
        )

    # information = []
    # # Создаем словарь с выходными параметрами
    # output_data = {
    #     "id": str(application_id),
    #     "telegram_id": telegram_id,
    #     "discord_id": discord_id,
    #     "email": data["email"],
    #     "phone": data["phone"],
    #     "name": data["name"],
    #     "surname": data["surname"],
    #     "patronymic": data["patronymic"],
    #     "university": data["university"],
    #     "student_group": data["student_group"],
    #     "title": data["title"],
    #     "adviser": data["adviser"],
    #     "applicant_role": data["applicant_role"],
    #     "submitted_at": submitted_at,
    #     "updated_at": updated_at,
    #     "coauthors": ", ".join(coauthors_list) if data["coauthors"] else None
    # }
    # information.append(output_data)
