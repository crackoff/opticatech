# -*- coding: utf-8 -*-

from flask_classy import FlaskView, route
from main import env


class AdminController(FlaskView):
    """ Контроллер для обслуживания страниц личного кабинета с моделями очков """

    sql_get_brands = """ """

    def index(self):
        template = env.get_template('models/list.html')
        return template.render()

    @route('/edit/<model_id>')
    def edit(self, model_id):
        """
        :type model_id: int
        """

        template = env.get_template('models/edit.html')
        ret = template.render()

        return ret
