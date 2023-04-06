from flask_restful import reqparse

change_password = reqparse.RequestParser()
change_password.add_argument(
    "password", help="This field cannot be blank", required=True
)

change_email = reqparse.RequestParser()
change_email.add_argument("email", help="This field cannot be blank", required=True)
