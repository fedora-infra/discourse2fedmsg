# -*- coding: utf-8 -*-
#
# This file is part of the Anitya project.
# Copyright (C) 2017-2020  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""
Tests for discourse2fedmsg.
"""
import hashlib
import hmac
import json
import unittest.mock as mock

import pytest
import os

import discourse2fedmsg as d2f


@pytest.fixture
def app():
    """
    Return the flask client.
    """
    return d2f.app.test_client()


def test_index(app):
    """
    Test for index function.
    """
    rv = app.get("/")

    assert rv.status_code == 200
    assert b"Source:  https://pagure.io/discourse2fedmsg" in rv.data


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
