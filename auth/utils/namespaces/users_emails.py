from flask_restx import Namespace, fields
from flask_restx import reqparse

ns = Namespace("Users emails", description="Users emails management. Route is only for Superusers and Admins")

emails = ns.model(
    "Emails",
    {
        "emails": fields.List(fields.String(readonly=True, description="Emails list"))
    },
)

users_id = reqparse.RequestParser()
users_id.add_argument("users_id", type=list, required=True, location="json")
