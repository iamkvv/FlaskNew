"""
Routes and views for the flask application.
ссылки:
https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3-ru
https://inloop.github.io/sqlite-viewer/
"""
 
from datetime import datetime
from flask import render_template,request, url_for, flash, redirect
from werkzeug.exceptions import abort

from FlaskNew import app
import sqlite3

import os.path

app.config['SECRET_KEY'] = '123456'

def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "database.db")
    print('base', BASE_DIR, db_path)

    conn = sqlite3.connect(db_path) #('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM 'posts'").fetchall()
    print(posts)
    conn.close()
    print(posts)

    return render_template(
        'index.html',
        title='Домашняя страница',
        year=datetime.now().year,
        posts = posts
    )

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Необходимо ввести заголовок')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

    return render_template('create.html')



@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Контакты',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
