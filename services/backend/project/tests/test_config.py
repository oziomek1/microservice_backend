import os
import unittest

from flask import current_app
from flask_testing import TestCase

from project import create_app


app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] == os.environ.get('SECRET_KEY'))
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL'))
        self.assertTrue(app.config['DEBUG_TB_ENABLED'])
        self.assertTrue(app.config['BCRYPT_LOG_ROUND'] == 4)
        self.assertTrue(app.config['TOKEN_EXPIRATION_DAYS'] == 0)
        self.assertTrue(app.config['TOKEN_EXPIRATION_SECONDS'] == 3600)


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == os.environ.get('SECRET_KEY'))
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_TEST_URL'))
        self.assertFalse(app.config['DEBUG_TB_ENABLED'])
        self.assertTrue(app.config['BCRYPT_LOG_ROUND'] == 4)
        self.assertTrue(app.config['TOKEN_EXPIRATION_DAYS'] == 0)
        self.assertTrue(app.config['TOKEN_EXPIRATION_SECONDS'] == 1)


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_app_is_production_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == os.environ.get('SECRET_KEY'))
        self.assertFalse(app.config['TESTING'])
        self.assertFalse(app.config['DEBUG_TB_ENABLED'])
        self.assertTrue(app.config['BCRYPT_LOG_ROUND'] == 12)
        self.assertTrue(app.config['TOKEN_EXPIRATION_DAYS'] == 0)
        self.assertTrue(app.config['TOKEN_EXPIRATION_SECONDS'] == 3600)


if __name__ == '__main__':
    unittest.main()
