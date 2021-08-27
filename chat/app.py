import functools
from re import S
from sqlite3.dbapi2 import Error
from flask.helpers import get_flashed_messages

from werkzeug.utils import redirect

from .db import get_db
from flask import Flask, config, render_template, request, session, Blueprint, g, flash
from .auth import login_required


bp = Blueprint('app', __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO post (author_id, body) VALUES (?, ?)',
                    (g.user['id'], request.form.get('post'))
        )
        db.commit()
    posts = db.execute('SELECT p.id, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created ASC')
    admin = db.execute('SELECT admin FROM user WHERE id=?', (g.user['id'],)).fetchone()['admin']
    return render_template('index.html', posts = posts, admin = admin)

@bp.route('/settings')
@login_required
def settings():
    return render_template('settings.html')