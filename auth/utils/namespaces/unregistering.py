from flask_restx import Namespace, fields

ns = Namespace("Unregistering", description="Here the user can delete himself.")

# user_id = ns.model(
#     "User",
#     {
#         "id": fields.String(
#             readonly=True, description="The login history UUID identifier"
#         )
#     },
# )