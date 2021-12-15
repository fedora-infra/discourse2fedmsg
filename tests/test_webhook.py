import hashlib
import hmac
import json

from discourse2fedmsg_messages import DiscourseMessageV1
from fedora_messaging import testing


def calc_sig(client, data):
    return hmac.new(
        client.config["DISCOURSE2FEDMSG_SECRET"].encode(),
        json.dumps(data).encode(),
        hashlib.sha256,
    ).hexdigest()


def test_webhook(app, client):
    data = {"ping": "OK"}
    headers = {
        "X-Discourse-Event-Signature": f"sha256={calc_sig(app, data)}",
        "X-Discourse-Event-Type": "ping",
        "X-Discourse-Event": "ping",
        "X-Discourse-Instance": "discourse.test",
        "X-Discourse-Event-Id": "1",
    }
    expected_body = {"webhook_body": data, "webhook_headers": headers}
    with testing.mock_sends(
        DiscourseMessageV1(topic="discourse.ping.ping", body=expected_body)
    ):
        rv = client.post(
            "/webhook",
            data=json.dumps(data),
            headers=headers,
        )

    assert rv.status_code == 200
    assert b"Everything is 200 OK" in rv.data


def test_webhook_remove_cooked_raw(app, client):
    data = {"ping": "OK", "post": {"cooked": "yummy", "raw": "eeew", "post_number": 11}}
    headers = {
        "X-Discourse-Event-Signature": f"sha256={calc_sig(app, data)}",
        "X-Discourse-Event-Type": "ping",
        "X-Discourse-Event": "ping",
        "X-Discourse-Instance": "discourse.test",
        "X-Discourse-Event-Id": "1",
    }
    # The body here should not have cooked or raw keys...
    expected_body = {
        "webhook_body": {"ping": "OK", "post": {"post_number": 11}},
        "webhook_headers": headers,
    }
    with testing.mock_sends(
        DiscourseMessageV1(topic="discourse.ping.ping", body=expected_body)
    ):
        rv = client.post(
            "/webhook",
            data=json.dumps(data),
            headers=headers,
        )

    assert rv.status_code == 200
    assert b"Everything is 200 OK" in rv.data


def test_webhook_missing_header(client):
    data = {"test_data": "data"}
    rv = client.post(
        "/webhook",
        data=json.dumps(data),
    )

    assert rv.status_code == 403
    assert b"No X-Discourse-Event-Signature found on request." in rv.data


def test_webhook_wrong_hash(app, client):
    data = {"test_data": "data"}
    rv = client.post(
        "/webhook",
        data=json.dumps(data),
        headers={
            "X-Discourse-Event-Signature": {calc_sig(app, data)},
            "X-Discourse-Event-Type": "test_event",
        },
    )

    assert rv.status_code == 400
    assert b"No sha256 prefix found." in rv.data


def test_webhook_not_valid_sig(client):
    data = {"test_data": "data"}
    rv = client.post(
        "/webhook",
        data=json.dumps(data),
        headers={
            "X-Discourse-Event-Signature": "sha256=abcde",
            "X-Discourse-Event-Type": "test_event",
        },
    )

    assert rv.status_code == 403
    assert b"Signature not valid." in rv.data
