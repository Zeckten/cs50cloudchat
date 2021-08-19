import functools
from re import S
from .db import get_db
from flask import Flask, config, render_template, request, session, Blueprint, g
from .auth import login_required


bp = Blueprint('home', __name__)


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
    return render_template('index.html', posts = posts )