from shared.controller import MainController
from .model import Account as AccountModel ,Role as RoleModel

account_controller = MainController(AccountModel)

def get_account(**kwargs):
    return account_controller.get_one(**kwargs)

def create_account(**kwargs):
    return account_controller.create(**kwargs)


role_controller = MainController(RoleModel)

def create_role(**kwargs):
    return role_controller.create(**kwargs)