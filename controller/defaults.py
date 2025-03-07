from account.model import Role as RoleModel
from shared.database import db
def create_default():
    create_default_roles()
    create_default_user()

def create_default_roles():
    from account.model import Role
    roles = ["admin", "teacher", "student", "parent"]
    
    for slug in roles:
        existing_role = Role.query.filter_by(slug=slug).first()
        if not existing_role:
            role = Role(slug=slug, name=slug.capitalize())
            db.session.add(role)
    
    db.session.commit()  



def create_default_user():
    from account.controller import create_account
    account = {
        "user_name":"ammar21",
        "email":"amar2003895@gmail.com",
        "password":"password",
        "phone_number":"07701648804",
        "full_name":"عمار هاني محمود",
        
    }
    try:
        account = create_account(**account)
        admin_role = RoleModel.query.filter_by(slug="admin").first()
        if admin_role:
            account.roles.append(admin_role)
            account.save() 
    except Exception as e:
        print(e)
        pass
    