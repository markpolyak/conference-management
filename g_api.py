from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.service_account import Credentials
from src.table_consts import *
from fastapi import FastAPI, UploadFile, File, Form
import io
import datetime

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
confSpreadSheetId = "1EbKtcUmpH-QC07cCoZBy8M4XWYU9CI_ag17kF59_RwY"
# ID папки Google Drive
gDriveFolderId = "1N8es1SMSAPxX6nSw-qSqVkaE6pi9B1Fl"
# Авторизуемся и получаем gSService и gDService — экземпляры доступа к API
credentials = Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes = ['https://www.googleapis.com/auth/drive'])

gSService = build('sheets', 'v4', credentials = credentials)
gDService = build('drive', 'v3', credentials = credentials)

# Получение полей по идентификатору (идентификатор равен строке)
def get_item_mathed_by_id(id, where, fields, fieldsDict):
    value = gSService.spreadsheets().values().get(
        spreadsheetId = where,
        range = (fieldsDict[fields[0]] + str(id) + ':' + fieldsDict[fields[len(fields) - 1]] + str(id)),
        majorDimension ='ROWS'
    ).execute()
    if 'values' not in value:
        return '-1'
    item = dict(zip(fields, value['values'][0]))
    if item['id'] != '':
        return item
    return '-1'

# Получение полей от и до
def get_items(where, start, end, fields, fieldsDict):
    values = gSService.spreadsheets().values().get(
        spreadsheetId = where,
        range = (fieldsDict[fields[0]] + str(start) + ':' + fieldsDict[fields[len(fields) - 1]] + str(end)),
        majorDimension ='ROWS'
    ).execute()
    if 'values' not in values:
        return '-1'
    res = []
    for item in values['values']:
        if not item:
            return res
        tuple = dict(zip(fields, item))
        if tuple['id'] != '':
            res.append(tuple)
    return res


# Загрузка файла на Google Disk
def upload_file_to_gDisk(file : UploadFile):  
    file_metadata = {
        'name': file.filename,
        'parents' : [gDriveFolderId]
    }
    content = file.file.read()
    media = MediaIoBaseUpload(io.BytesIO(content), mimetype='application/msword', resumable=True)
    uploadedF = gDService.files().create(body=file_metadata, media_body=media,
                    fields='id').execute()
    return uploadedF.get('id')

def update_publication_fields(sheetId, applicationId,
    fileId = None, publication_title = None, keywords = None, abstract = None):
    uplFields = {}
    if not (fileId is None):
        uplFields.update({
            'review_status' : 'in progress',
            'download_url' : ('https://docs.google.com/document/d/' + fileId),
            'upload_date' : datetime.datetime.now().astimezone().isoformat()
        })
    if not (publication_title is None):
        uplFields['publication_title'] = publication_title
    if not (keywords is None):
        uplFields['keywords'] = keywords
    if not (abstract is None):
        uplFields['abstract'] = abstract

    update = []
    for key, value in uplFields.items():
        range = requestsSheetFields[key] + str(applicationId) + ':'+  requestsSheetFields[key] + str(applicationId)
        update.append({
            'range' : range,
            'majorDimension' : 'ROWS',
            'values' : [[value]]
        })
    
    values = gSService.spreadsheets().values().batchUpdate(
        spreadsheetId=sheetId,
        body = {
            "valueInputOption": "USER_ENTERED",
            "data": update
        }   
    ).execute()