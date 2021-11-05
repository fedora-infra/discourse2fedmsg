import os

import pytest

from discourse2fedmsg.app import create_app


@pytest.fixture
def app(tmpdir):
    app = create_app()
    app.config.from_object("tests.app_config")
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client
