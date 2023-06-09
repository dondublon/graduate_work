from http import HTTPStatus

from flask import current_app
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from flask_restful import Resource

from resources.parsers.auth import register_parser, auth_parser
from services.user_service import UserService, JWTs
from utils.namespaces import registration, login, refresh, logout, unregistering
from utils.namespaces.login import tokens
from utils.parsers.auth import access_token_required, refresh_token_required
from utils.parsers.login import credentials
from utils.parsers.registration import register_data
from utils.token import check_if_token_in_blacklist


@registration.ns.route("")
@registration.ns.expect(register_data)
class Registration(Resource):
    @registration.ns.marshal_with(tokens, code=HTTPStatus.CREATED)
    def post(self):
        """Register user"""
        data = register_parser.parse_args()
        payload, status = UserService.register(**data)
        return payload, status


@login.ns.route("")
@login.ns.expect(credentials)
class Authorization(Resource):
    @login.ns.marshal_with(tokens)
    def post(self):
        """Authorization by credentials"""
        data = auth_parser.parse_args()
        payload, status = UserService.login(data["email"], data["password"], data.get("User-Agent"), data.get("Device"))
        if status == HTTPStatus.OK and isinstance(payload, JWTs):
            current_app.logger.info(f"{data['email']} successful authorization")
            return payload.dict(), status
        return payload, status


@refresh.ns.route("")
@refresh.ns.expect(refresh_token_required)
class RefreshToken(Resource):
    @refresh.ns.marshal_with(tokens)
    @jwt_required(refresh=True)
    @check_if_token_in_blacklist()
    def post(self):
        user_id = get_jwt_identity()
        refresh_token = get_jwt()
        payload, status = UserService.refresh(user_id, refresh_token)
        if status == HTTPStatus.OK and isinstance(payload, JWTs):
            return payload.dict(), status
        return payload, status


@logout.ns.route("")
@logout.ns.expect(access_token_required)
class Logout(Resource):
    @jwt_required(verify_type=False)
    @check_if_token_in_blacklist()
    def post(self):
        user_id = get_jwt_identity()
        payload = get_jwt()
        payload, status = UserService.logout(user_id, payload)
        return payload, status


@unregistering.ns.route("")
@unregistering.ns.expect(access_token_required)
class Unregistering(Resource):
    # @registration.ns.marshal_with(tokens, code=HTTPStatus.OK)
    @jwt_required(verify_type=False)
    def delete(self):
        """Unregister user (delete them)"""
        user_id = get_jwt_identity()
        try:
            result = UserService.unregister(user_id)
            status = HTTPStatus.OK if result else HTTPStatus.NOT_FOUND
        except:
            status = HTTPStatus.INTERNAL_SERVER_ERROR
        return {"user_id": user_id}, status
