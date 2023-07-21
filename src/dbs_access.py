from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.service_account import Credentials
from src.tables_settings import *
from fastapi import UploadFile
import io
import datetime
from pprint import pprint

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
confSpreadsheetId = "1EbKtcUmpH-QC07cCoZBy8M4XWYU9CI_ag17kF59_RwY"
# ID папки Google Drive
gDriveFolderId = "1N8es1SMSAPxX6nSw-qSqVkaE6pi9B1Fl"
# Авторизуемся и получаем gSService и gDService — экземпляры доступа к API
credentials = Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes = ['https://www.googleapis.com/auth/drive'])

gSService = build('sheets', 'v4', credentials = credentials)
gDService = build('drive', 'v3', credentials = credentials)

# fromR и toR (включительно) задаются с учетом смещения из fieldsParams
# т.е. отдельно учитывать смещение не нужно
def make_range(fromR, toR, field, fieldsParams):
    if (fieldsParams['rowOffset'] + toR) > maxRNum \
        or (fieldsParams['rowOffset'] + fromR) > maxRNum:
        raise IndexError('Row exceeds grid limits.')
    start = 'R' + str(fieldsParams['rowOffset'] + fromR) \
    + 'C' + str(fieldsParams['colOffset'] + fieldsParams['fields'][field] + 1)
    end = 'R' + str(fieldsParams['rowOffset'] + toR) \
    + 'C' + str(fieldsParams['colOffset'] + fieldsParams['fields'][field] + 1)
    return start + ':' + end

# Получение полей от и до с присутствующим значением параметра
def get_items_by_par(spreadsheetId, fromR : int, toR : int, par : dict, fields : set, fieldsParams : dict):
    try:
        par['value'] = str(par['value'])
        ranges = []
        # Упорядочивание полей для сравнения по 0 полю
        fields = list(fields - {par['name'] ,'id'})
        idPos = 0
        mainParPos = 1
        fields.insert(idPos, 'id')
        fields.insert(mainParPos, par['name'])
        for field in fields:
            ranges.append(make_range(fromR, toR, field, fieldsParams))

        values = gSService.spreadsheets().values().batchGet(
            spreadsheetId = spreadsheetId,
            ranges = ranges,
            majorDimension ='COLUMNS'
        ).execute()

        if 'valueRanges' not in values:
            return '-1'
        items = []
        # Подсчет кол-ва элементов
        if 'values' in values['valueRanges'][idPos] \
            and 'values' in values['valueRanges'][mainParPos]:
            itemsCount = min(
                len(values['valueRanges'][idPos]['values'][0]),
                len(values['valueRanges'][mainParPos]['values'][0])
            )
        else:
            return items
        
        for curItem in range(itemsCount):
            fieldsArr = []
            # Проверка на существование (если есть id и соответствует ли он строке)
            if values['valueRanges'][idPos]['values'][0][curItem] != str(fromR + curItem):
                continue
            # Проверка главного параметра на равенство необходимому значению
            if values['valueRanges'][mainParPos]['values'][0][curItem] != par['value']:
                continue

            for curField in range(len(values['valueRanges'])):
                if 'values' in values['valueRanges'][curField]:
                    curItemsCount = len(values['valueRanges'][curField]['values'][0])
                    if curItem >= curItemsCount:
                        fieldsArr.append('')
                    else:
                        fieldsArr.append(values['valueRanges'][curField]['values'][0][curItem])
                else:
                    fieldsArr.append('')
            
            items.append(dict(zip(fields, fieldsArr)))
        return items

    except IndexError as IE:
        return '-1'

# Получение полей по идентификатору (идентификатор равен строке)
def get_item_by_id(spreadsheetId : str, itemId : int, fields : set, fieldsParams : dict):
    item = get_items_by_par(
            spreadsheetId,
            itemId, itemId,
            {'name' : 'id', 'value' : itemId},
            fields,
            fieldsParams)
    if item == '-1' or not item:
        return '-1'
    else:
        return item[0]
        
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
        range = make_range(
            applicationId, applicationId,
            key,
            table['appAndPub']
        )
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