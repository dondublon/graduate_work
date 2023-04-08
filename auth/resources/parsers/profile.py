from flask_restful import reqparse

change_password = reqparse.RequestParser()
change_password.add_argument(
    "password", help="This field cannot be blank", required=True
)

change_email = reqparse.RequestParser()
change_email.add_argument("email", help="This field cannot be blank", required=True)

change_profile = reqparse.RequestParser()
change_profile.add_argument("first_name", help="", required=True)
change_profile.add_argument("family_name", help="= last_name", required=True)
change_profile.add_argument("father_name", help="", required=True)
change_profile.add_argument("phone", help="phone", required=True)