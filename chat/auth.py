import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db, create_invite

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        invite = request.form['invite']
        username = request.form['username']
        password = request.form['password']
        confirmation = request.form['confirmation']
        db = get_db()
        error = None

        if not invite:
            error = 'Invite is required.'
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirmation:
            error = 'Passwords do not match.'
        
        try:
            admin = db.execute('SELECT admin FROM invite WHERE code=?', (invite,)).fetchone()['admin']
        except:
            error = 'Invalid invite'
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, admin) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), admin),
                )
                db.execute('DELETE FROM invite WHERE code=?', (invite,))
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        db = get_db()
        if db.execute('SELECT admin FROM user WHERE id=?', g.user['id']) == 0:
            return redirect('/')

        return view(**kwargs)

    return wrapped_view


@bp.route('/invite', methods=['GET'])
@login_required
def invite():
    invite = None
    if request.args.get('submit', str) == 'Admin':
        invite = create_invite(1)
    elif request.args.get('submit', str) == 'User':
        invite = create_invite(0)
    else:
        return ('error', request.args.get('submit'))
    return ('Your invite code is %s' % str(invite))

@bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    db = get_db()
    if request.method == "POST":
        oldpassword = request.form['oldpassword']
        newpassword = request.form['newpassword']
        confirmation = request.form['confirmation']
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE id = ?', (g.user['id'],)
        ).fetchone()
        if not oldpassword:
                error = 'Password is required.'
        elif not check_password_hash(user['password'], oldpassword):
            error = 'Incorrect password.'
        elif newpassword != confirmation:
            error = 'Passwords do not match.'
        if error == None:
                db.execute('UPDATE user SET password = ? WHERE id = ?', (generate_password_hash(newpassword), g.user['id']))
                db.commit()
                flash('Password Changed')
        else:
            flash(error)

    return render_template('settings.html')