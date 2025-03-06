from account.model import Role as RoleModel
def create_default():
    create_default_role()
    create_default_user()

def create_default_role():
    from account.controller import create_role
    create_role(slug="admin")
    create_role(slug="teacher")
    create_role(slug="student")
    create_role(slug="parent")

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
    