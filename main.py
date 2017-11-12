# -*- coding: utf-8 -*-

import os

from flask import Flask, send_from_directory, render_template
from jinja2 import Environment, PackageLoader

app = Flask(__name__, template_folder='views')
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='a@mail.ru',
    PASSWORD='19216801'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
env = Environment(loader=PackageLoader('main', 'views'))


# Регистрация страниц ошибок
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('errors/500.html'), 500


# Регистрация контроллеров
from database import init_db
from controllers import admin, application
admin.AdminController.register(app, route_base='/admin/')
application.AppController.register(app, route_base='/app/')


# @app.route('/init/')
def init():
    """ Сервисный метод для инициализации базы данных """
    init_db()
    return "Done"


@app.route('/')
def index():
    """ Главная страница сайта """
    return render_template('landing.html')


@app.route('/contact')
def contact():
    """ Главная страница сайта """
    return render_template('landing.html')


@app.route('/assets/<path:path>')
def assets(path):
    """ Папка с внешними компонентами """
    return send_from_directory('assets', path)


@app.route('/images/<path:path>')
def image(path):
    """ Папка с изображениями """
    return send_from_directory('images', path)


if __name__ == '__main__':
    app.run()
