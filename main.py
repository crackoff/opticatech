# -*- coding: utf-8 -*-

import os

from flask import Flask, send_from_directory
from jinja2 import Environment, PackageLoader

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
env = Environment(loader=PackageLoader('main', 'views'))


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
    template = env.get_template('landing.html')
    return template.render()


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
