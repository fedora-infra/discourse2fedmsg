from flask import Blueprint

from discourse2fedmsg.utils import import_all


blueprint = Blueprint("root", __name__)
import_all("discourse2fedmsg.views")

