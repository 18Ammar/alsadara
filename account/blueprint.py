from flask import Blueprint,request

account = Blueprint("account",__name__)

@account.get("/")
def get_account():
    return "get account"
