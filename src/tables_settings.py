# Параметры таблиц
# Необходимо заполнить в соответствии с расположением в таблице
table = {
    'conf' : {
        "rowOffset" : 1,
        "colOffset" : 0,
        "fields" : [ 
            "id",
            "apps_spreadsheet_id",
            "registration_end_date",
            "submission_end_date"
        ]
    },

    'appAndPub' : {
        "rowOffset" : 1,
        "colOffset" : 0,
        "fields" : [ 
            "id",
            "telegram_id",
            "discord_id" ,
            "email",
            "publication_title" ,
            "upload_date" ,
            "review_status",
            "download_url",
            "keywords" ,
            "abstract"
        ]
    }
}

# Максимальное кол-во строк в таблице
maxRNum = 1000

def initialize_table(table):
    fieldsDict = {}
    for fieldPos in range(len(table['fields'])):
        fieldsDict[table['fields'][fieldPos]] = fieldPos
    table['fields'] = fieldsDict

def filtrate_fields(fieldsDict, filter):
    tuple = {}
    for field in fieldsDict:
        if field in filter:
            tuple[field] = fieldsDict[field]
    return tuple

def initialize_tables():
    for curTab in table:
       initialize_table(table[curTab])

# Используется для получения выборок параметров в запросах
selection = {
    # Поля выборки конференции
    'conf' : {
        "id",
        "apps_spreadsheet_id",
        "registration_end_date",
        "submission_end_date"
    },
    # Поля выборки публикации по id
    'pub' : {
        "id",
        "publication_title" ,
        "upload_date" ,
        "review_status",
        "download_url",
        "keywords" ,
        "abstract"
    },
    # Поля выборки публикации по параметру
    'shortPub' : {
        "id",
        "publication_title" ,
        "upload_date" ,
        "review_status"
    }
}