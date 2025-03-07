class BaseException(Exception):
    code = 500
    def __init__(self,message:dict):
        super().__init__(message.get("en") if isinstance(message,dict) else message)
        self.msg = message.get("en") if isinstance(message,dict) else message
        self.msg_ar = message.get("ar") if isinstance(message,dict) else message


class InvalidRequest(BaseException):
    def __init__(self, *args:object)->None:
        super().__init__(*args)
        self.code = 400
    

class NotFound(BaseException):
    def __init__(self, *args:object)->None:
        super().__init__(*args)
        self.code = 404

class NotAuthenticated(BaseException):
    def __init__(self, *args):
        super().__init__(*args)
        self.code = 401

class UnauthorizedAccount(BaseException):
    def __init__(self, *args:object)->None:
        super().__init__(*args)
        self.code = 403