from flask_restx import Namespace, fields
from flask_restx import reqparse

ns = Namespace(
    "Profile",
    description="Here the user can get information about his profile and change it",
)
user = ns.model(
    "User",
    {
        "id": fields.String(
            readonly=True, description="The login history UUID identifier"
        ),
        "email": fields.String(readonly=True),
    },
)

email = reqparse.RequestParser()
email.add_argument("email", type=str, required=True, location="json")

password = reqparse.RequestParser()
password.add_argument("password", type=str, required=True, location="json")
