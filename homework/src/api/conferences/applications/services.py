from gspread import service_account

from settings import PROJECT_FILE_PATH

SAMPLE_SPREADSHEET_ID = '1PT-q0EvdZ21P7MN598qtE0cuWyleMSX0aGieuahmyH4'

def get_worksheet(identif_id):
    gc = service_account(filename=PROJECT_FILE_PATH)
    return gc.open_by_key(identif_id).sheet1

def append_to_worksheet(row_values,identif_id, worksheet=None):
    if worksheet is None:
        worksheet = get_worksheet(identif_id)


    worksheet.append_row(row_values)
    return True
