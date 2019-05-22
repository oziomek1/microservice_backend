from project import db
from sqlalchemy.sql import func


class BlacklistToken(db.Model):
    __tablename__ = 'blacklist_token'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return '<id: {} token: {}'.format(self.id, self.token)

    @staticmethod
    def check_blacklist(auth_token):
        result = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        return True if result else False
