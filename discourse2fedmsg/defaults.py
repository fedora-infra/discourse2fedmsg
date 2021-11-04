# This file contains the default configuration values

TEMPLATES_AUTO_RELOAD = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///../discourse2fedmsg.db"

HEALTHZ = {
    "live": "discourse2fedmsg.utils.healthz.liveness",
    "ready": "discourse2fedmsg.utils.healthz.readiness",
}
