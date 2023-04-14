from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT

from core.config import logger
from models_backend.models import Movie, Review, InsertedSuccessModel, DeletedCountSuccessModel, \
    ReviewSuccessModel, ObjectsListSuccessModel
from services.reviews import Reviews
from starlette.requests import Request

from .common import check_auth

COLLECTION_NAME = "reviews"
router_reviews = APIRouter(prefix=f"/{COLLECTION_NAME}")


@router_reviews.post("/add")
async def add_review(review: Review, request: Request):
    """
    An example request JSON:
    {
    "movie": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    "text" : "......"
    }
    We assume that request headers contain used_uuid, after processing with authentication and middleware.
    Headers:
        ...
        user_uuid: d16b19e7-e116-43b1-a95d-cd5a11e8f1b4
        ...
    """
    user_uuid = request.headers.get("user_uuid")
    try:
        result = await Reviews.add(user_uuid, review)
        logger.info("Successfully added %s, user=%s, %s=%s", COLLECTION_NAME, user_uuid, COLLECTION_NAME, review)
        return InsertedSuccessModel(success=True, inserted_id=str(result.inserted_id))
    except Exception as e:
        logger.error(
            "Error adding %s, user=%s, %s=%s, error=%s", COLLECTION_NAME, user_uuid, COLLECTION_NAME, review, e
        )
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router_reviews.delete("/remove")
async def remove_review(movie: Movie, request: Request, authorize: AuthJWT = Depends()):
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
        result = await Reviews.remove(user_uuid, movie)
        logger.info("Successfully deleted %s, user=%s, movie=%s", COLLECTION_NAME, user_uuid, movie)
        return DeletedCountSuccessModel(success=True, deleted_count=str(result.deleted_count))
    except Exception as e:
        logger.error("Error removing %s, user=%s, movie=%s, error=%s", COLLECTION_NAME, user_uuid, movie, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router_reviews.get("/get")
async def get_review(movie: Movie, request: Request, authorize: AuthJWT = Depends()):
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
        review = await Reviews.get(user_uuid, movie)
        if review is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        logger.info("Successfully got %s, user=%s, movie=%s", COLLECTION_NAME, user_uuid, movie)
        return ReviewSuccessModel(success=True, text=review["text"], time=review["time"])
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting %s, user=%s, movie=%s, error=%s", COLLECTION_NAME, user_uuid, movie, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router_reviews.get("/list")
async def list_reviews(movie: Movie, request: Request, authorize: AuthJWT = Depends()):
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
    + Optional request parameter
        sort: likes_count | average_rate
    """
    # TODO Make pagination.
    user_uuid = (await check_auth(request, authorize)).user_uuid
    try:
        sort_way = request.query_params.get("sort")
        reviews_list = await Reviews.list(movie, sort_way)
        success = True
        logger.error(
            "Successfylly listed %s, user=%s, movie=%s, sort_way=%s", COLLECTION_NAME, user_uuid, movie, sort_way
        )
        return ObjectsListSuccessModel(success=success, objects_list=reviews_list)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error listing %s, user=%s, movie=%s, error=%s", COLLECTION_NAME, user_uuid, movie, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


