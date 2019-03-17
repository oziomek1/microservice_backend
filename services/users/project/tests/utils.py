from project import db
from project.api.models import User


def add_user(username, email, password, admin=False):
    user = User(
        username=username,
        email=email,
        password=password,
    )
    db.session.add(user)
    db.session.commit()

    if admin:
        user = User.query.filter_by(email=email).first()
        user.admin = True
        db.session.commit()
    return user
