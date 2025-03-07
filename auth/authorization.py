import jwt
from jwt import ExpiredSignatureError
from uuid import uuid4
from account.controller import get_account
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os
from passlib.hash import pbkdf2_sha256
from shared.exceptions import UnauthorizedAccount
from shared.response import messages
load_dotenv(".env")

def create_account_token(account:dict,remember=True,subject="login")->str:
    assert {'id','user_name','phone_number','roles'}.issubset(account.keys()),"Account must have id, email and role"
    payload={
        'iat':datetime.utcnow(),
        'exp':datetime.utcnow()+timedelta(days=30) if remember else datetime.utcnow()+timedelta(days=1),
        'sub':subject,
        'id':account['id'],
        'jti':str(uuid4()),
        
    }
    token = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')
    return token

def get_token_data(token:str, subject:str= None)->dict:
    token_type,token=token.split()
    if token_type != "Bearer":
        raise Exception("Invalid token type")
    try:
        data=jwt.decode(jwt=token,key=os.getenv("SECRET_KEY"), algorithms=["HS256"])
    except ExpiredSignatureError:
        raise Exception("Expired token")
    return data

def get_user_by_token(token:str,subject=None)->dict:
    data = get_token_data(token=token)
    try:
        account =  get_account(data['account_id'])
        return account
    except:
        raise Exception("this user is not exist")



def check_password(account,password):
    if pbkdf2_sha256.verify(password, account.password):
        return True
    raise UnauthorizedAccount(messages["Invalid login credentials"])