# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_classy import FlaskView, route
import sqlite3
from database import get_db
from main import env, app


class AdminController(FlaskView):
    """ Контроллер для обслуживания страниц личного кабинета с моделями очков """

    sql_get_brands = """ """

    def index(self):
        if not session.get('logged_in'):
            return redirect('/admin/login')
        db = get_db()
        cur = db.execute('SELECT id, title, text FROM entries ORDER BY id DESC')
        entries = cur.fetchall()
        return render_template('models/list.html', entries=entries)

    @route('/add', methods=['POST'])
    def add_entry(self):
        if not session.get('logged_in'):
            abort(401)
        db = get_db()
        db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
                   [request.form['title'], request.form['text']])
        db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('index'))

    @route('/edit/<model_id>')
    def edit(self, model_id):
        """
        :type model_id: int
        """

        ret = render_template('models/edit.html')

        return ret

    @route('/login', methods=['GET', 'POST'])
    def login(self):
        error = None
        if request.method == 'POST':
            if request.form['username'] != app.config['USERNAME']:
                error = 'Пользователь не найден'
            elif request.form['password'] != app.config['PASSWORD']:
                error = 'Неверный пароль'
            else:
                session['logged_in'] = True
                flash('Вы вошли в личный кабинет')
                return redirect('/admin')
        return render_template('login.html', error=error)

    @route('/register', methods=['GET', 'POST'])
    def reg(self):
        error = None
        if request.method == 'POST':
            if request.form['username'] != app.config['USERNAME']:
                error = 'Пользователь не найден'
            elif request.form['password'] != app.config['PASSWORD']:
                error = 'Неверный пароль'
            else:
                session['logged_in'] = True
                flash('Вы вошли в личный кабинет')
                return redirect('/admin')
        return render_template('register.html', error=error)

    @route('/logout')
    def logout(self):
        session.pop('logged_in', None)
        flash('You were logged out')
        return redirect('/')
