import json

from flask_restful import reqparse

users_id_parser = reqparse.RequestParser()
users_id_parser.add_argument("users_id", help="This field cannot be blank", required=True, action="append")
