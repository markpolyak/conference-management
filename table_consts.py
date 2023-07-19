# Параметры таблиц
confsSheetFields = {}
confsSheetFieldsSeq = [ 
    "id",
    "requests_sheet_id",
    "registration_end_date",
    "submission_end_date"
]

requestsSheetFields = {}
requestsSheetFieldsSeq = [
    "id",
    "telegram_id",
    "discord_id" ,
    "email" ,
    "publication_title" ,
    "upload_date" ,
    "review_status",
    "download_url",
    "keywords" ,
    "abstract"
]

publicationSheetFieldsSet = {
    "id",
    "publication_title" ,
    "upload_date" ,
    "review_status",
    "download_url",
    "keywords" ,
    "abstract"
}
shortPublicationSheetFieldsSet = {
    "id",
    "publication_title" ,
    "upload_date" ,
    "review_status"
}

def initialize_table_consts():
    startAt = 'A'
    for i in range(len(confsSheetFieldsSeq)):
        confsSheetFields[confsSheetFieldsSeq[i]] = chr(ord(startAt) + i)

    startAt = 'A'  
    for i in range(len(requestsSheetFieldsSeq)):
        requestsSheetFields[requestsSheetFieldsSeq[i]] = chr(ord(startAt) + i)
