from flask import Blueprint

index_blue = Blueprint("index", __name__,template_folder="./templates")

from . import views
