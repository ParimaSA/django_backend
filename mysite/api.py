import helpers
from ninja import Schema

from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.add_router("customer/", "customer.api.router")
api.add_router("business/", "business.api.router")


class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # is not requst.user.is_authenticated
    email: str = None

@api.get("/hello")
def hello(request):
    # print(request)
    return {"message":"Hello World"}

@api.get("/me",
    response=UserSchema,
    auth=helpers.api_auth_user_or_guest)
def me(request):
    return request.user