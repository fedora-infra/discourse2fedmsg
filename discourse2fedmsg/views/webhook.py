import hashlib
import hmac
import json
from logging import disable

from discourse2fedmsg_messages import DiscourseMessageV1
from fedora_messaging.api import Message, publish
from fedora_messaging.exceptions import ConnectionException, PublishReturned
from flask import current_app, request
from jsonschema.exceptions import ValidationError

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

    body = {}
    header_list = ["X-Discourse-Instance", "X-Discourse-Event-Id", "X-Discourse-Event-Type", "X-Discourse-Event", "X-Discourse-Event-Signature"]
    body["webhook_headers"] = {headername: request.headers[headername] for headername in header_list}
    body["webhook_body"] =  json.loads(payload)

    topic = f"discourse.{body['webhook_headers']['X-Discourse-Event-Type']}.{body['webhook_headers']['X-Discourse-Event']}"

    try:
        msg = DiscourseMessageV1(
            topic=topic,
            body=body,
        )
        publish(msg)
    except PublishReturned as e:
        error = f"Fedora Messaging broker rejected message {msg.id}: {e}"
        current_app.logger.warning(error)
    except ConnectionException as e:
        error = f"Error sending message {msg.id}: {e}"
        current_app.logger.warning(error)
    except ValidationError as e:
        error = f"Error validating Fedora Message schema {msg.id}: {e}"
        current_app.logger.warning(error)
        return error, 403

    return "Everything is 200 OK"
