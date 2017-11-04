# -*- coding: utf-8 -*-

from flask_classy import FlaskView, route
from flask import request
from main import env
import base64
import json
import numpy as np
import cv2
from imgproc import get_detected


class AppController(FlaskView):
    """ Контроллер для обслуживания приложения онлайн-примерочной """

    @route('/<model_id>')
    def index(self, model_id):
        """
        Главная и единственная страница собсвенно приложения
        :type model_id: int
        """
        template = env.get_template('app.html')
        return template.render()

    @route('/process', methods=['GET', 'POST'])
    def process(self):
        if request.method == 'POST':
            args = json.loads(request.data)

            b = args['img']
            bin = base64.b64decode(str(b.split(",")[1]))
            image = np.asarray(bytearray(bin), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)

            image = get_detected(image)

            a = base64.b64encode(cv2.imencode('.jpg', image)[1])

            return "data:image/webp;base64,{}".format(a)
        else:
            return 'Use POST method'
