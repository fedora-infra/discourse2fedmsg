""" discourse2fedmsg.py

This is a small Flask app designed to receive the POST webhook callbacks fired
by Discourse.  Upon receiving a POST, this webapp will try to verify
that it actually came from discourse and then republish the payload to our own
fedmsg bus.

This started off as a fork of https://github.com/fedora-infra/zanata2fedmsg

Author:     Ralph Bean <rbean@redhat.com>
            Patrick Uiterwijk <puiterwijk@redhat.com>
License:    GPLv2+
"""

import hmac
import hashlib
import json
import os

import fedmsg
import flask

import logging
log = logging.getLogger()

app = flask.Flask(__name__)

secret = os.environ.get('DISCOURSE2FEDMSG_SECRET', 'CHANGEME')

if secret == 'CHANGEME':
    raise Exception('Please provide a secret via DISCOURSE2FEDMSG_SECRET env')


@app.route('/')
def index():
    return "Source:  https://pagure.io/discourse2fedmsg"


@app.route('/webhook', methods=['POST'])
def webhook():
    header_sig = flask.request.headers.get('X-Discourse-Event-Signature', None)

    if not header_sig:
        error = 'No X-Discourse-Event-Signature found on request.'
        return error, 403

    if not header_sig.startswith('sha256='):
        return 'No sha256 prefix found.', 400
    header_sig = header_sig[len('sha256='):]

    payload = flask.request.data

    calced_sig = hmac.new(
        secret,
        payload,
        hashlib.sha256
    ).hexdigest()
    log.info('Comparing %r with %r' % (header_sig, calced_sig))

    if header_sig != calced_sig:
        return 'Signature not valid.', 403

    payload = json.loads(payload)
    log.info('Payload: %r' % payload)

    # Crazy enough..... they don't seem to have this in the signed portion of
    # the payload.... At least not per the docs...
    topic = flask.request.headers.get('X-Discourse-Event-Type', None)
    log.info('Topic: %s' % topic)

    return "Testing before sending"

    # Having verified the message, we're all set.  Republish it on our bus.
    fedmsg.publish(
        modname='discourse',
        topic=topic,
        msg=payload,
    )
    return "Everything is 200 OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
