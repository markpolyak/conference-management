import uvicorn

from fastapi import FastAPI, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.router import router

app = FastAPI()
app.include_router(router=router)


# TODO пересмотреть идею где хранить exception_handlers
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
