from fastapi import APIRouter, Depends

from schema import Application, ApplicationCreate

router = APIRouter(
    prefix="/conferences/{conference_id}/applications",
    tags=["Applications"]
)


@router.get("/", response_model=list[Application])
def get_applications(conference_id: int):
    pass


@router.post("/", response_model=Application)
def post_application(conference_id: int, application: ApplicationCreate):
    pass

# TODO разобраться с тем, как определить параметры пути для обновления и удаления
#   записей по tg or ds or email
@router.put("/")
def put_application():
    pass


@router.delete("/")
def del_application():
    pass
