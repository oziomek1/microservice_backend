import pytest

from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

from src import create_app
from src import db
from src.api.models.user import User


@pytest.fixture(scope="session")
def app(request):
    """
    Returns session-wide application.
    """
    _app = create_app()
    # _app.config.from_object('src.config.TestingConfig')
    return _app


@pytest.fixture(scope="session")
def test_client(app, request):
    """
    Returns session-wide initialised database.
    """
    with app.app_context():
        db.drop_all()
        db.create_all()


@pytest.fixture(scope="module", autouse=True)
def session(app, test_client, request):
    """
    Returns function-scoped session.
    """
    with app.app_context():
        conn = db.engine.connect()
        texec = conn.begin()

        session = db.create_scoped_session(
            options=dict(bind=conn, binds={})
        )

        # establish  a SAVEPOINT just before beginning the test
        # (http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
        session.begin_nested()

        @event.listens_for(session(), 'after_transaction_end')
        def restart_savepoint(sess2, trans):
            # Detecting whether this is indeed the nested transaction of the test
            if trans.nested and not trans._parent.nested:
                # The test should have normally called session.commit(),
                # but to be safe we explicitly expire the session
                sess2.expire_all()
                session.begin_nested()

        db.session = session
        yield session

        # Cleanup
        session.remove()
        # This instruction rollsback any commit that were executed in the tests.
        texec.rollback()
        conn.close()


@pytest.fixture(scope="module")
def new_user():
    user = User(
        username="user_tester",
        email="user_tester@mail.com",
        password="tester_password",
    )
    return user
