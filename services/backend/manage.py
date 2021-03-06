import logging
import unittest

import coverage
from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models.user import User
from project.api.models.admin import Admin


COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()


app = create_app()
cli = FlaskGroup(create_app=create_app)

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('test')
def test():
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command('seed_db')
def seed_db():
    db.session.add(User(
        username='Adam',
        email='adam@email.com',
        password='adam_password',
    ))
    db.session.add(User(
        username='Jennifer',
        email='jenny@email.com',
        password='jenny_password',
    ))
    db.session.add(Admin(
        username="Josiek",
        email="josiek@email.com",
        password="josiek_password",
    ))
    db.session.add(Admin(
        username="Wojtes",
        email="wojtes@email.com",
        password="wojtes_password",
    ))
    db.session.commit()


@cli.command('test_coverage')
def test_coverage():
    """Unit tests with coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    cli()