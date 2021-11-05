import hashlib
import hmac
import json

from fedora_messaging.api import Message, publish
from fedora_messaging.exceptions import ConnectionException, PublishReturned
from flask import current_app, request

from . import blueprint as bp


@bp.route("/webhook", methods=["POST"])
def webhook():
    current_app.logger.error("triggered")
    secret = current_app.config["DISCOURSE2FEDMSG_SECRET"]

    header_sig = request.headers.get("X-Discourse-Event-Signature", None)

    if not header_sig:
        error = "No X-Discourse-Event-Signature found on request."
        return error, 403

    if not header_sig.startswith("sha256="):
        return "No sha256 prefix found.", 400
    header_sig = header_sig[len("sha256=") :]

    payload = request.data

    calced_sig = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    current_app.logger.info(f"Comparing {header_sig!r} with {calced_sig!r}")

    if header_sig != calced_sig:
        return "Signature not valid.", 403

    payload = json.loads(payload)

    event_type = request.headers.get("X-Discourse-Event-Type", None)
    event = request.headers.get("X-Discourse-Event", None)

    topic = f"discourse.{event_type}.{event}"

    current_app.logger.info("Topic: %s" % topic)
    # current_app.logger.info("Payload: %s" % payload)
    # return "Testing before sending"

    # Having verified the message, we're all set.  Republish it on our bus.
    try:
        msg = Message(
            topic=topic,
            body=payload,
        )
        publish(msg)
    except PublishReturned as e:
        current_app.logger.warning(
            "Fedora Messaging broker rejected message %s: %s", msg.id, e
        )
    except ConnectionException as e:
        current_app.logger.warning("Error sending message %s: %s", msg.id, e)

    return "Everything is 200 OK"
