from http import HTTPStatus

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from mill_sime.config import setting
from mill_sime.domain.exceptions import AlreadyExistsError, NotFoundError
from mill_sime.primary.routes import farmer

app = FastAPI(
    title=setting.project_name,
)
app.include_router(router=farmer.router)


@app.exception_handler(NotFoundError)
def handle_not_found(_request: Request, exc: NotFoundError) -> Response:
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={"message": str(exc)},
    )


@app.exception_handler(AlreadyExistsError)
def handle_already_exists(_request: Request, exc: AlreadyExistsError) -> Response:
    return JSONResponse(
        status_code=HTTPStatus.CONFLICT,
        content={"message": str(exc)},
    )
