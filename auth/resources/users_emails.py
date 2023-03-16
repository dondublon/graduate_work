from flask_jwt_extended import jwt_required
from flask_restful import Resource

from resources.parsers.users_emails import users_id_parser
from services.emails_service import EmailService
from utils.decorators import roles_required
from utils.namespaces.users_emails import ns, emails, users_id
from utils.parsers.auth import access_token_required


@ns.route("")
@ns.expect(access_token_required)
class UsersEmailsResource(Resource):
    @ns.marshal_list_with(emails)
    @ns.expect(users_id)
    @jwt_required()
    @roles_required("Admin")
    def get(self):
        """Get list of user rights"""
        data = users_id_parser.parse_args()
        emails = EmailService.get_user_roles(data["users_id"])
        return emails
