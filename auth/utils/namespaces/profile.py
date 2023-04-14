from flask_restx import Namespace, fields
from flask_restx import reqparse

ns = Namespace(
    "Profile",
    description="Here the user can get information about his profile and change it",
)
user = ns.model(
    "User",
    {
        "id": fields.String(readonly=True, description="The login history UUID identifier"),
        "email": fields.String(readonly=True),
    },
)

user_profile = ns.model(
    # Without email
    "User",
    {
        "id": fields.String(readonly=True, description="The login history UUID identifier"),
        "first_name": fields.String(readonly=True),
        "family_name": fields.String(readonly=True),
        "father_name": fields.String(readonly=True),
        "phone": fields.String(readonly=True),
    },
)

email = reqparse.RequestParser()
email.add_argument("email", type=str, required=True, location="json")

password = reqparse.RequestParser()
password.add_argument("password", type=str, required=True, location="json")
