from http import HTTPStatus

from fastapi_jwt_auth import AuthJWT

from brokers.rabbitmq_publish import rabbitmq_publish
from core.config import settings, logger
from fastapi import APIRouter, HTTPException, Depends
from models_backend.models import ReviewId, ReviewLike, UpsertedSuccessModel, DeletedCountSuccessModel, LikesSetSuccessModel
from services.review_likes import ReviewLikes
from starlette.requests import Request

from .common import check_auth

COLLECTION_NAME = "review_likes"
router_reviewlikes = APIRouter(prefix=f"/{COLLECTION_NAME}")


@router_reviewlikes.post("/add")
async def add_like(like: ReviewLike, request: Request, authorize: AuthJWT = Depends()):
    """
    An example request JSON:
    {
    "review": "63ff480aa96c3ea499bc01242",
    "movie":  "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    "review_author_id": "d96f4d59-12d4-419c-967d-fd62c41cc6b0",
    "value": 5
    }
    We assume that request headers contain used_uuid, after processing with authentication and middleware.
    Headers:
        ...
        user_uuid: d16b19e7-e116-43b1-a95d-cd5a11e8f1b4
        ...
    """
    user_uuid = (await check_auth(request, authorize)).user_uuid
    if not (0 <= like.value <= 10):
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Value must be from 0 to 10.s")
    try:
        result = await ReviewLikes.add(user_uuid, like)

        success = True
        logger.info("Successfully added %s, user=%s, %s=%s", COLLECTION_NAME, user_uuid, COLLECTION_NAME, like)
        payload = {"author_id": str(like.review_author_id), "event_type": "review_like"}
        http_result = UpsertedSuccessModel(success=success, upserted_id=str(result.upserted_id))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    try:
        await rabbitmq_publish(settings.rabbitmq_host, settings.rabbitmq_queue, payload)
    except Exception as e:
        logger.error("Error sengins to the %s: %s", settings.rabbitmq_host, e)
        try:
            await rabbitmq_publish(settings.rabbitmq_host_dlq, settings.rabbitmq_queue, payload)
        except Exception as e2:
            logger.error("Error sengins to the %s: %s", settings.rabbitmq_host_dlq, e2)
    return http_result


@router_reviewlikes.delete("/remove")
async def remove_like(review: ReviewId, request: Request, authorize: AuthJWT = Depends()):
    """
    An example request JSON:
    {
    "id": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    }
    We assume that request headers contain used_uuid, after processing with authentication and middleware.
    Headers:
        ...
        user_uuid: d16b19e7-e116-43b1-a95d-cd5a11e8f1b4
        ...
    """
    user_uuid = (await check_auth(request, authorize)).user_uuid
    try:
        result = await ReviewLikes.remove(user_uuid, review)
        logger.info("Successfully deleted %s, user=%s, review=%s", COLLECTION_NAME, user_uuid, review)
        return DeletedCountSuccessModel(success=True, deleted_count=str(result.deleted_count))
    except Exception as e:
        logger.error(
            "Error removing %s, user=%s, %s=%s, error=%s", COLLECTION_NAME, user_uuid, COLLECTION_NAME, review, e
        )
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router_reviewlikes.get("/count")
async def count_likes(review: ReviewId, request: Request, authorize: AuthJWT = Depends()):
    """
    An example request JSON:
    {
    "id": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    }
    We assume that request headers contain used_uuid, after processing with authentication and middleware.
    Headers:
        ...
        user_uuid: d16b19e7-e116-43b1-a95d-cd5a11e8f1b4
        ...
    """
    user_uuid = (await check_auth(request, authorize)).user_uuid
    try:
        count, average = ReviewLikes.count(review=review)
        logger.info("Succesfully counted %s, user=%s, review=%s", COLLECTION_NAME, user_uuid, review)
        return LikesSetSuccessModel(success=True, count=count, average=average)
    except Exception as e:
        logger.error("Error counting %s, user=%s, review=%s, error=%s", COLLECTION_NAME, user_uuid, review, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
