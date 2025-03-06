import jwt
from uuid import uuid4
from account.controller import get_account

def create_account_token(account:dict,remember=True,subject="login")->str:
    assert {'id','user_name','phone_number','role'}.issubset(account.keys()),"Account must have id, email and role"
    payload={
        'iat':datetime.utcnow(),
        'exp':datetime.utcnow()+timedelta(days=30) if remember else datetime.utcnow()+timedelta(days=1),
        'sub':subject,
        'id':account['id'],
        'jti':str(uuid4()),
        
    }
    token = jwt.encode(payload,app.config['SECRET_KEY'],algorithm='HS256')
    return token

def get_token_data(token:str, subject:str= None)->dict:
    token_type,token=token.split()
    if token_type != "Bearer":
        raise Exception("Invalid token type")
    try:
        data=jwt.decode(jwt=token,key=os.getenv("JWT_SECRET"), algorithms=["HS256"])
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



