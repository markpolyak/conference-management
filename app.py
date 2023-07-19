from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse

from src.table_consts import *
from main import app
from src.auxiliary import *
from src.g_api import upload_file_to_gDisk, update_publication_fields

@app.get("/conferences/{conference_id}/publications")
def get_user_publications(conference_id: int, email = None, telegram_id: int = None, discord_id: int = None):
    #try:
        confFields = conf_actions(conference_id)
        if 'status' in confFields:
            return JSONResponse(status_code=confFields['status'])
        
        authPar = check_auth(email, telegram_id, discord_id)
        if not authPar:
            return JSONResponse(status_code=404)
        
        publications = get_requests_by_auth(
            confFields['requests_sheet_id'],
            authPar,
            requestsSheetFieldsSeq,
            requestsSheetFields
        )
        if publications:
            return publications
        return JSONResponse(status_code=404)
    #except Exception as e:
    #    return {"status" : 500}



@app.get("/conferences/{conference_id}/applications/{application_id}/publication")
def get_publication_by_id(conference_id: int,application_id : int, email = None, telegram_id: int = None, discord_id: int = None):
        confFields = conf_actions(conference_id)
        if 'status' in confFields:
            return JSONResponse(status_code=confFields['status'])
        
        authPar = check_auth(email, telegram_id, discord_id)
        if not authPar:
            return JSONResponse(status_code=404)
        
        publication = get_publication(confFields['requests_sheet_id'], application_id, authPar)
        if 'status' in publication:
            return JSONResponse(status_code = publication['status'])
        return publication


@app.post("/conferences/{conference_id}/applications/{application_id}/publication")
def post_publication(conference_id: int, application_id : int,
        publication_title = Form(...), file : UploadFile = File(...),
        email = Form(None), discord_id : int = Form(None), telegram_id : int = Form(None),
        keywords = Form(None), abstract = Form(None)
        ):

        confFields = conf_actions(conference_id)
        if 'status' in confFields:
            return JSONResponse(status_code=confFields['status'])

        authPar = check_auth(email, telegram_id, discord_id)
        if not authPar:
            return JSONResponse(status_code=404)
        
        application = get_publication(confFields['requests_sheet_id'], application_id, authPar)
        if 'status' in application:
            return JSONResponse(status_code=application['status'])
        
        fileId = upload_file_to_gDisk(file)
        update_publication_fields(
            confFields['requests_sheet_id'],
            application_id,
            fileId,
            publication_title,
            keywords,
            abstract)

        return get_publication(confFields['requests_sheet_id'], application_id, authPar)


@app.put("/conferences/{conference_id}/applications/{application_id}/publication")
def put_publication(conference_id: int, application_id : int,
        email = None, discord_id : int = None, telegram_id : int = None,
        file : UploadFile = File(...),
        ):

        confFields = conf_actions(conference_id)
        if 'status' in confFields:
            return JSONResponse(status_code=confFields['status'])

        authPar = check_auth(email, telegram_id, discord_id)
        if not authPar:
            return JSONResponse(status_code=404)
        
        application = get_publication(confFields['requests_sheet_id'], application_id, authPar)
        if 'status' in application:
            return JSONResponse(status_code=application['status'])
        
        fileId = upload_file_to_gDisk(file)
        update_publication_fields(
            confFields['requests_sheet_id'],
            application_id,
            fileId)

        return get_publication(confFields['requests_sheet_id'], application_id, authPar)

@app.patch("/conferences/{conference_id}/applications/{application_id}/publication")
def patch_publication(conference_id: int, application_id : int,
        email = Form(None), discord_id : int = Form(None), telegram_id : int = Form(None),
        publication_title = Form(None), keywords = Form(None), abstract = Form(None)
        ):

        confFields = conf_actions(conference_id)
        if 'status' in confFields:
            return JSONResponse(status_code=confFields['status'])

        authPar = check_auth(email, telegram_id, discord_id)
        if not authPar:
            return JSONResponse(status_code=404)
        
        application = get_publication(confFields['requests_sheet_id'], application_id, authPar)
        if 'status' in application:
            return JSONResponse(status_code=application['status'])
        
        update_publication_fields(
            confFields['requests_sheet_id'],
            application_id,
            publication_title = publication_title,
            keywords = keywords,
            abstract = abstract
        )

        return get_publication(confFields['requests_sheet_id'], application_id, authPar)
        