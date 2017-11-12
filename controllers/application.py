# -*- coding: utf-8 -*-

from flask_classy import FlaskView, route
from flask import request, render_template, abort, session
from main import env
import base64
import json
import numpy as np
import cv2
from imgproc import get_mixed
from database import get_db


class AppController(FlaskView):
    """ Контроллер для обслуживания приложения онлайн-примерочной """

    @route('/<model_id>')
    def index(self, model_id):
        """
        Главная и единственная страница собственно приложения
        :type model_id: int
        """
        db = get_db()
        cur = db.execute('SELECT id, title, text FROM entries WHERE id = ?', [model_id])
        model = cur.fetchone()

        if model is None:
            abort(404)

        return render_template('app.html', model=model)

    @route('/process', methods=['GET', 'POST'])
    def process(self):
        """
        Сервисный метод для обработки видео-потока
        """
        if request.method == 'POST':
            args = json.loads(request.data)
            model_id = int(args["model_id"])
            specs = cv2.imread('images/database/{}.png'.format(model_id), -1)

            image = args["img"]
            image = base64.b64decode(str(image.split(",")[1]))
            image = np.asarray(bytearray(image), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            image = get_mixed(image, specs, session)
            image = base64.b64encode(cv2.imencode('.jpg', image)[1])

            return "data:image/jpeg;base64,{}".format(image)
        else:
            return 'Use POST method'
