import hashlib
import hmac
import json

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
    current_app.logger.info("Payload: %r" % payload)

    # Crazy enough..... they don't seem to have this in the signed portion of
    # the payload.... At least not per the docs...
    topic = request.headers.get("X-Discourse-Event-Type", None)
    current_app.logger.info("Topic: %s" % topic)
    current_app.logger.info("Payload: %s" % payload)
    # return "Testing before sending"

    # Having verified the message, we're all set.  Republish it on our bus.
    fedmsg.publish(
        modname="discourse",
        topic=topic,
        msg=payload,
    )
    return "Everything is 200 OK"
