from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from fastapi_jwt_auth import AuthJWT
import orjson
from fastapi_pagination import Page, paginate
from starlette.requests import Request

from core.config import logger
from paginate_model.paginate_models import ProfilesOut
from services.user import UserService, NotFoundError
from .common import check_auth, check_role
from models_backend.models import UserRegisterModel, ChangeEmailModel, UserProfilesModel, UserBasic
from helpers.reply import reply_to_dict


router_user = APIRouter(prefix=f"/user")


# noinspection PyUnusedLocal
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
                                            user.family_name, user.father_name,
                                            user.email, user.phone)

        success = True
        logger.info("Successfully added user %s", user)
        return orjson.dumps({"success": success, "inserted_id": str(result.id_),
                             "access_token": result.access_token, "refresh_token": result.refresh_token})
    except Exception as e:
        logger.error("Error adding %s, error=%s", user, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router_user.post('/update-profile')
async def update_profile(user: UserBasic, request: Request, authorize: AuthJWT = Depends()):
    """No email"""
    # NOT TESTED YET!
    user_id = (await check_auth(request, authorize)).user_uuid

    try:
        result = await UserService.update_profile(user_id, user.first_name,
                                            user.family_name, user.father_name,
                                            user.phone)

        success = True
        logger.info("Successfully updated user %s", user)
        return orjson.dumps({"success": success})
    except Exception as e:
        logger.error("Error updating %s, error=%s", user, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router_user.post('/change-email')
async def change_email(user: ChangeEmailModel, request: Request, authorize: AuthJWT = Depends()):
    """No email"""
    auth_result = await check_auth(request, authorize)

    try:
        result = await UserService.change_email(auth_result.access_token, auth_result.user_uuid,
                                            user.email)

        success = True
        logger.info("Successfully updated email for user %s to %s", auth_result.user_uuid, user.email)
        return orjson.dumps({"success": success, "new email": user.email})
    except Exception as e:
        logger.error("Error changing email %s, error=%s", user, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router_user.get('/get-profile')
async def get_profile(request: Request, authorize: AuthJWT = Depends()):
    """No email"""
    auth_result = await check_auth(request, authorize)
    try:
        result = await UserService.get_profile(auth_result.user_uuid)
        if result is None:
            raise NotFoundError(f"User {auth_result.user_uuid} not found.")
        logger.info("Successfully got profile for user %s", auth_result.user_uuid)
        return orjson.dumps(reply_to_dict(result))
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error("Error getting id %s, error=%s", auth_result.user_uuid, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router_user.get('/profiles', response_model=Page[ProfilesOut])
async def get_profiles(users: UserProfilesModel, request: Request, authorize: AuthJWT = Depends()):
    """Request to Profiles service"""
    auth_result = await check_auth(request, authorize)
    roles_list = await check_role(auth_result.user_uuid, auth_result.access_token)
    try:
        result = await UserService.get_profiles(users.users_id)
        logger.info("Successfully get profiles for users %s", users.users_id)
        return paginate(result)
    except Exception as e:
        logger.error("Error get profiles %s, error=%s", users.users_id, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router_user.delete('/delete-user')
async def delete_user(request: Request, authorize: AuthJWT = Depends()):
    auth_result = await check_auth(request, authorize)
    try:
        await UserService.delete_user(auth_result.access_token, auth_result.user_uuid)
    except Exception as e:
        logger.error("Error deleting user %s, error=%s", auth_result.user_uuid, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

@router_user.get('/avatar',
                 responses={200: {"content": {"image/png": {}, "image/jpeg": {}}}},
                 response_class=Response
                 )
async def get_avatar(request: Request, authorize: AuthJWT = Depends()):
    # auth_result = await check_auth(request, authorize)  # Temporary
    result = await UserService.get_avatar('auth_result.user_uuid')
    return Response(content=result.chunk_data, media_type="image/jpeg")
