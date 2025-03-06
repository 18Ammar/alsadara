from base.abstract.model import BaseModel
from shared.database import db
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.orm import validates
from passlib.hash import pbkdf2_sha256

class Account(BaseModel):
    __tablename__ = 'accounts'
    user_name = db.Column(db.String(88),unique=False,nullable=False,comment='the user name of the account must match [a-zA-Z0-9_]')
    password = db.Column(db.String(200),nullable=False,comment='user Password hashed using ppkdf2_sha256') 
    email = db.Column(db.String(255),unique=True,comment='user email')
    full_name = db.Column(db.String(255),nullable=False)
    phone_number = db.Column(db.String(255),nullable=False)
    roles = db.relationship("Role",secondary='account_roles',back_populates='accounts')
    
    @validates('user_name')
    def validate_user_name(self,key,value):
        if not value.isalnum():
            raise ValueError('user name must be alphanumeric')
        return value
    @validates('email')
    def validate_email(self,key,value):
        if not '@' in value:
            raise ValueError('invalid email')
        return value


    @validates("password")
    def validate_password(self,key,value):
        if len(value) < 8:
            raise ValueError('password must be at least 8 characters')
        return pbkdf2_sha256.hash(value)

    def has_role(self,role):
        return bool(
            Role.query.join(Role.accounts).filter(
                Account.id == self.id,
                Role.slug == role
            ).count() > 0
        )
    


class Role(BaseModel):
    __tablename__ = 'roles'
    name = db.Column(db.String(255),unique=True,nullable=False)
    slug = db.Column(db.String(255),unique=True,nullable=False,comment="this is a unique identifier for the role")
    accounts = db.relationship("Account",secondary='account_roles',back_populates='roles')

class AccountRole(BaseModel):
    __tablename__ = 'account_roles'
    user_id = db.Column(db.String(255),db.ForeignKey('accounts.id'),primary_key=True)
    role_id = db.Column(db.String(255),db.ForeignKey('roles.id'),primary_key=True)