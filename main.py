import uvicorn

from fastapi import FastAPI, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.responses import JSONResponse
from src.schema import Application, ApplicationCreate, ApplicationUpdate


app = FastAPI()

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    val_errors = exc.errors()
    for err in val_errors:
        if "email" in err["loc"]:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"message": f"{err['type']}: {err['ctx']['reason']}", "body": str(err)}
            )
        elif "phone" in err["loc"]:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"message": f"{err['type']}: {err['msg']}", "body": str(err)}
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"message": f"{err['type']}: {err['loc'][1]} {err['ctx']['error']}", "body": str(err)}
            )
        
        

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/applications", response_model=Application, status_code=status.HTTP_201_CREATED)
def create_application(application: ApplicationUpdate):
    return Application(**application.model_dump())


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1 ", port=8000)


