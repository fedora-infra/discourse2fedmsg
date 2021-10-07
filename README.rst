Try it out
----------

Prepare virtual env::

    python -m venv .venv
    source .venv/bin/activate

Install app with dependencies::

    pip install .

Run the server::

    $ DISCOURSE2FEDMSG_SECRET=CHANGEME python discourse2fedmsg.py


Testing
-------

This app is using `tox` for testing.

Install tox (Fedora)::

    dnf install tox

Run the tests::

    tox
