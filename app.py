""" app.py

This is a small wrapper for openshift deployments.
Author:     Patrick Uiterwijk <puiterwijk@redhat.com>
License:    GPLv2+
"""

from discourse2fedmsg import app
app.run(host='0.0.0.0', port=8080)
