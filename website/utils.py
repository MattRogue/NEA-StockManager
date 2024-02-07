
def create_staff(email: str,
        password: str,
        firstname: str,
        surname: str,
        type: str) :
        
    from .models import Staff, StaffType, generate_password_hash
    from . import db
    
    if Staff.query.filter_by(email = email).first():
        return False
    
    try:
        type = StaffType[type.upper()]
    except KeyError:
        raise Exception("KeyError: StaffType accepts only TEMP, TEACHER, HEAD")
        return False
    
    user = Staff(email = email,
        password = generate_password_hash(password),
        firstname = firstname,
        surname = surname,
        type = type)
    db.session.add(user)
    db.session.commit()
    return user

def check_staff(email: str, password: str) -> bool:
    from .models import Staff, check_password_hash
    user = Staff.query.filter_by(email = email).first()
    if user and check_password_hash(user.password, password):
        return user
    return False