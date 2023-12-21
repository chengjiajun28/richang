from flask import Blueprint

admin_blue = Blueprint("admin", __name__,template_folder="./templates")

from . import views
