import hashlib
import hmac
import json
import unittest.mock as mock

import pytest
from flask import current_app


@mock.patch("fedmsg.publish")
def test_webhook(mock_publish, app):
    data = {"test_data": "data"}
    calced_sig = hmac.new(
        d2f.secret.encode(), json.dumps(data).encode(), hashlib.sha256
    ).hexdigest()
    rv = app.post(
        "/webhook",
        data=json.dumps(data),
        headers={
            "X-Discourse-Event-Signature": "sha256=" + calced_sig,
            "X-Discourse-Event-Type": "test_event",
        },
    )

    assert rv.status_code == 200
    assert b"Everything is 200 OK" in rv.data

    mock_publish.assert_called_with(modname="discourse", topic="test_event", msg=data)


def test_webhook_missing_header(app):
    data = {"test_data": "data"}
    rv = app.post(
        "/webhook",
        data=json.dumps(data),
    )

    assert rv.status_code == 403
    assert b"No X-Discourse-Event-Signature found on request." in rv.data


def test_webhook_wrong_hash(app):
    data = {"test_data": "data"}
    calced_sig = hmac.new(
        d2f.secret.encode(), json.dumps(data).encode(), hashlib.sha256
    ).hexdigest()
    rv = app.post(
        "/webhook",
        data=json.dumps(data),
        headers={
            "X-Discourse-Event-Signature": calced_sig,
            "X-Discourse-Event-Type": "test_event",
        },
    )

    assert rv.status_code == 400
    assert b"No sha256 prefix found." in rv.data


def test_webhook_not_valid_sig(app):
    data = {"test_data": "data"}
    rv = app.post(
        "/webhook",
        data=json.dumps(data),
        headers={
            "X-Discourse-Event-Signature": "sha256=abcde",
            "X-Discourse-Event-Type": "test_event",
        },
    )

    assert rv.status_code == 403
    assert b"Signature not valid." in rv.data
