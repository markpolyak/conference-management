from pprint import pprint
from src.table_consts import *
from src.g_api import *

# Получение полей публикации по параметрам аутентификации
# Удаляются параметры аутентификации
def get_requests_by_auth(requestsSheetId, authPar, fields, fieldsDict):
    values = get_items(requestsSheetId, 1, 1001, requestsSheetFieldsSeq, requestsSheetFields)
    res = []
    for tuple in values:
        if tuple[authPar['name']] == authPar['value'] \
            and 'upload_date' in tuple:
                if tuple['upload_date'] != '':
                    res.append(filtrate_fields(tuple, shortPublicationSheetFieldsSet))
    return res

def check_auth(email, telegram_id, discord_id):
    authPar = check_params([
            {'name' : 'email', 'value' : email},
            {'name' : 'telegram_id', 'value' : telegram_id},
            {'name' : 'discord_id', 'value' : discord_id}
    ])
    if authPar['ok']:
        return authPar
    return []


# Проверка корректности параметров
# Может и должен присутствовать только один параметр
def check_params(params):
    authPar = {"ok" : False, "name" : "", "value" : ""}
    for param in params:
        if param['value'] and authPar['ok'] and param['value'] != None:
            authPar['ok'] = False
            return authPar
        if param['value'] and param['value'] != None:
            authPar['ok'] = True
            authPar['name'] = param['name']
            authPar['value'] = param['value']
    authPar['value'] = str(authPar['value'])
    return authPar

def conf_actions(conference_id):
    confFields = get_item_mathed_by_id(
        str(conference_id),
        confSpreadSheetId,
        confsSheetFieldsSeq,
        confsSheetFields
    )
    if confFields == '-1':
        return {'status' : 404}
    
    endTime = datetime.datetime.strptime(confFields['registration_end_date'], '%d.%m.%Y')
    endTime += datetime.timedelta(hours = 23, minutes = 59)
    if endTime <= datetime.datetime.now():
        return {'status' : 403}
    return confFields
    

def filtrate_fields(fieldsDict, filter):
    tuple = {}
    for field in fieldsDict:
        if field in filter:
            tuple[field] = fieldsDict[field]
    return tuple

def filtrate_fields_arr(fieldsDictArr, filter):
    res = []
    for item in fieldsDictArr:
        tuple = {}
        for field in item:
            if field in filter:
                tuple[field] = item[field]
    return res

def add_fields(fieldsDictArr, fieldsAdd):
    for item in fieldsDictArr:
        for field in fieldsAdd:
            if field not in item:
                item[field] = ''

def get_publication(requestSheetId, applicationId, authPar):
    application = get_item_mathed_by_id(applicationId, requestSheetId, requestsSheetFieldsSeq, requestsSheetFields)
    if application == '-1':
        return {'status' : 404}
    if application[authPar['name']] != authPar['value']:
        return {'status' : 403}
    application = filtrate_fields(application, publicationSheetFieldsSet)
    return application
