from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object("web.secure")
    app.config.from_object("web.setting")

    from 网站.web.modules.index import index_blue
    app.register_blueprint(index_blue)

    from 网站.web.modules.admin import admin_blue
    app.register_blueprint(admin_blue)

    return app
