from flask import Blueprint
from shared.request import Request
from .controller import get_account
from shared.exceptions import NotFound,NotAuthenticated
from shared.response import messages
from auth.authorization import check_password,create_account_token
from auth.decorators import required_login
from .model import Role as RoleModel
from .controller import create_account


account = Blueprint("account",__name__)

@account.post("/")
@required_login("admin")
def create_account_endpoint(*args, **kwargs):
    data = Request(required_args={"user_name","email","password","full_name","phone_number","role",})
    data["email"] = data["email"].lower()
    account_data = {
        "user_name": data["user_name"],
        "email": data["email"],
        "password": data["password"],
        "full_name": data["full_name"],
        "phone_number": data["phone_number"],
    }
    try:
        account = create_account(**account_data)
        user_role = RoleModel.query.filter_by(slug=data["role"]).first()
        if user_role:
            account.roles.append(user_role)
            account.save()
    except Exception as e:
        raise NotFound(messages["Account creation failed"])
    token = create_account_token(account.get())
    body = {
        "token": token,
        "account": account.get()
    }
    return body
    


@account.post("/login")
def login():
    data = Request(required_args={"login","password"})
    password = data["password"]
    if "@" in data["login"]:
        data = {
            "email":data["login"]
        }
        data["email"] = data["email"].lower()
    else:
        data={
            "user_name":data["login"]
        }
    try:
        account = get_account(**data)
        
    except NotFound:
        raise NotAuthenticated(messages["Login credential is invalid"])
        
    check_password(account,password)
    token = create_account_token(account.get())
    body = {
        "token":token,
        "account":account.get()
    }

    return body

