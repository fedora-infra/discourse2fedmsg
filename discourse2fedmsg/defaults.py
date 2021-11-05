# This file contains the default configuration values

TEMPLATES_AUTO_RELOAD = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True

HEALTHZ = {
    "live": "discourse2fedmsg.utils.healthz.liveness",
    "ready": "discourse2fedmsg.utils.healthz.readiness",
}
