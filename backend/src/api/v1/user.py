from http import HTTPStatus

from fastapi import APIRouter, HTTPException
import orjson
from starlette.requests import Request

from core.config import logger
from services.user import UserService
from .common import check_auth
from models.models import UserRegisterModel

router_user = APIRouter(prefix=f"/user")


@router_user.post('/register')
async def register(user: UserRegisterModel, request: Request):
    """
    An example request JSON:
    {
    # TODO Fill in,
    }
    We assume that request headers contain used_uuid, after processing with authentication and middleware.
    Headers:
        ...
        user_uuid: d16b19e7-e116-43b1-a95d-cd5a11e8f1b4
        ...
    """
    try:
        result = await UserService.register(user.password, user.password_confirmation, user.first_name,
                                            user.last_name, user.father_name,
                                            user.email, user.phone)

        success = True
        logger.info("Successfully added user %s", user)
    except Exception as e:
        logger.error("Error adding %s, error=%s", user, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps({"success": success, "inserted_id": str(result.id_)})

