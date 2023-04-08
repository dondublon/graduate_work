import logging

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, get_unverified_jwt_headers
from flask_restful import Resource

from resources.parsers.profile import change_password, change_email, change_profile
from services.user_service import UserService
from utils.namespaces.profile import ns, user, email, password, user_profile
from utils.parsers.auth import access_token_required
from utils.token import check_if_token_in_blacklist


@ns.route("/change-password")
@ns.expect(access_token_required, password)
class ChangePassword(Resource):
    @jwt_required()
    @check_if_token_in_blacklist()
    def post(self):
        """Change password"""
        data = change_password.parse_args()
        user_id = get_jwt_identity()
        payload, status = UserService.change_password(user_id, data["password"])
        return payload, status


#  TODO Change email in Profiles service (gRPC)
@ns.route("/change-email")
@ns.expect(access_token_required, email)
class ChangeEmail(Resource):
    @jwt_required(refresh=True)
    @check_if_token_in_blacklist()
    def post(self):
        """Change login"""
        data = change_email.parse_args()
        user_id = get_jwt_identity()
        full = get_jwt()
        #header = get_unverified_jwt_headers()
        logging.info('get_jwt_identity %s', user_id)
        logging.info('get_jwt %s', full)  # decoded
        #logging.info('header %s', header)  # alg, typ
        raw_token = request.headers['Authorization']
        logging.info('Authorization %s', raw_token)
        payload, status = UserService.change_email(user_id, data["email"])
        return payload, status


@ns.route("/change-profile")
@ns.expect(access_token_required)
class ChangeProfile(Resource):
    """Change profile without email."""
    @ns.marshal_with(user_profile)
    @jwt_required()
    @check_if_token_in_blacklist()
    def post(self):
        """Change login"""
        data = change_profile.parse_args()
        user_id = get_jwt_identity()

        payload, status = UserService.change_profile(user_id, **data)
        return payload, status


@ns.route("")
@ns.expect(access_token_required)
class Profile(Resource):
    @ns.marshal_with(user)
    @jwt_required()
    @check_if_token_in_blacklist()
    def get(self):
        """Get user profile"""
        user_id = get_jwt_identity()
        user_instance = UserService.get_user_profile(user_id)
        return user_instance.as_dict
