from flask import render_template

from 网站.web.modules.admin import admin_blue


@admin_blue.route('/hah')
def index():
    return render_template("a.html")
