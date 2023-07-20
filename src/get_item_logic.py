from src.tables_settings import *
from src.dbs_access import *

def get_conference(conferenceId):
    confFields = get_item_by_id(confSpreadsheetId, conferenceId, selection['conf'], table['conf'])
    if confFields == '-1':
        return {'status' : 404}
    
    endTime = datetime.datetime.strptime(confFields['registration_end_date'], '%d.%m.%Y')
    endTime += datetime.timedelta(hours = 23, minutes = 59)
    if endTime <= datetime.datetime.now():
        return {'status' : 403}
    return confFields


def get_application(appsSheetId, appId, authPar):
    application = get_item_by_id(appsSheetId, appId, authPar['name'], table['appAndPub'])
    if application == '-1':
        return {'status' : 404}
    if application[authPar['name']] != authPar['value']:
        return {'status' : 403}
    return application


def get_publication(appsSheetId, appId, authPar):
 
    fields = {authPar['name']}
    fields.update(selection['pub'])

    application = get_item_by_id(appsSheetId, appId, fields, table['appAndPub'])
    if application == '-1':
        return {'status' : 404}
    if application[authPar['name']] != authPar['value']:
        return {'status' : 403}

    publication = filtrate_fields(application, selection['pub'])
    return publication

# Получение полей публикации по параметрам аутентификации
# Только с непустым полем 'upload_date'
def get_publications_by_auth(spreadsheetId, authPar, fields, fieldsParams):
    values = get_items_by_par(
        spreadsheetId,
        1, maxRNum - fieldsParams['rowOffset'],
        authPar,
        fields,
        fieldsParams)
    res = []
    if values == '-1':
        return []

    for tuple in values:
        if tuple['upload_date'] != '':
            res.append(filtrate_fields(tuple, selection['shortPub']))
    return res

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

def check_auth(email, telegram_id, discord_id):
    authPar = check_params([
            {'name' : 'email', 'value' : email},
            {'name' : 'telegram_id', 'value' : telegram_id},
            {'name' : 'discord_id', 'value' : discord_id}
    ])
    if authPar['ok']:
        return authPar
    return {'status' : 405}
