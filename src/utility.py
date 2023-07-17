from typing import Union, List, Optional

import gspread
from gspread import Worksheet

from src.schema import Application, ApplicationCreate


def open_by_key(key: str):
    gs = gspread.service_account()
    return gs.open_by_key(key).sheet1


def parse_record(record: list, sheet: Worksheet) -> Application:
    field_names = sheet.row_values(1)

    return Application(**{field_name: field for field_name, field in zip(field_names, record)})


def parse_records(records: List[list], sheet: Worksheet) -> List[Application]:
    for record in records:
        record = parse_record(record, sheet)

    return records


def find_record_by_id(record_id: int, sheet: Worksheet) -> Application:
    record_coord = sheet.find(str(record_id))

    if record_coord:
        record = sheet.row_values(record_coord.row)
        record = parse_record(record)
        print(record)
        return record


def find_record_by_tg_ds_or_email(param: str, sheet: Worksheet) -> List[Application]:
    records_coords = sheet.findall(param)

    if records_coords:
        records = [sheet.row_values(coord.row) for coord in records_coords]
        records = parse_records(records, sheet)
        print(records)
        return records
    

# TODO Посмотреть как будет устроен запрос на удаление
def del_record_by_id(record_id: int, param: str, sheet: Worksheet) -> Application:
    record = find_record_by_id(record_id, sheet)
    pass


def update_record_by_id(record_id: int, body: ApplicationCreate, sheet: Worksheet) -> Application:
    record: Optional[Application] = find_record_by_id(record_id, sheet)

    if record:
        if record.telegram_id == body.telegram_id:
            pass # TODO Дописать функцию добавления записи в таблицу
        elif record.discord_id == body.telegram_id:
            pass
        elif record.email == body.email:
            pass
        else:
            return # TODO Обратока ошибки


if __name__ == "__main__":
    find_record_by_tg_ds_or_email(("1010"), open_by_key("11HX661IUFybGlWWrxJUCkSlRooGTPhl1rpyqXsxirmU"))
