from flask import Blueprint
from shared.request import Request
from .controller import get_account
from shared.exceptions import NotFound,NotAuthenticated
from shared.response import messages
from auth.authorization import check_password,create_account_token
account = Blueprint("account",__name__)

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
