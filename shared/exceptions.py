class BaseException(Exception):
    code = 500
    def __init__(self, message:dict):
        super().__init__(message.get("en") if isinstance(message,dict) else message)
        self.msg=message.get("en") if isinstance(message,dict) else message
        self.msg_ar=message.get("ar") if isinstance(message,dict) else message

class InvalidRequest(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.code=400

class NotAuthenticated(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.code=401

class NotLoggedIn(NotAuthenticated):
    pass

class InvalidToken(NotAuthenticated):
    pass

class MissingToken(NotAuthenticated):
    pass

class RevokedToken(NotAuthenticated):
    pass

class ExpiredToken(NotAuthenticated):
    pass

class InvalidSubject(NotAuthenticated):
    pass

class InvalidSignature(NotAuthenticated):
    pass

class Forbidden(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.code=403

class UnauthorizedAccount(Forbidden):
    pass

class OperationNotPermitted(Forbidden):
    pass

class NotFound(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.code=404

class MethodNotAllowed(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.code=405

class ValidationError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.code=406

class NotAcceptable(ValidationError):
    pass

class NotUniqueError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.code=409

class AlreadyExists(NotUniqueError):
    pass
