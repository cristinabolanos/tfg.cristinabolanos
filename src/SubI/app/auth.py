
import functools
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		name = request.form['name']
		subname = request.form['subname']
		db = get_db()
		error = None

		if not email:
			error = 'Email is required.'
		elif not password:
			error = 'Password is required.'
		elif not name:
			error = 'Name is required.'
		elif not subname:
			error = 'Subname is required.'
		elif db.execute(
			'SELECT EMAIL FROM USER WHERE EMAIL = ?', (email,)
		).fetchone() is not None:
			error = 'User {} is already registered.'.format(email)

		if error is None:
			db.execute(
				'INSERT INTO USER (EMAIL, PASSWORD, NAME, SUBNAME) VALUES (?, ?, ?, ?)',
				(email, generate_password_hash(password), name, subname)
			)
			db.commit()
			return redirect(url_for('auth.login'))

		flash(error)

	return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute(
			'SELECT * FROM USER WHERE EMAIL = ?', (email,)
		).fetchone()

		if user is None:
			error = 'Incorrect email.'
		elif not check_password_hash(user['PASSWORD'], password):
			error = 'Incorrect password.'

		if error is None:
			session.clear()
			session['user_id'] = user['EMAIL']
			return redirect(url_for('hello'))

		flash(error)

	return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM USER WHERE EMAIL = ?', (user_id,)
		).fetchone()

@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('hello'))

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view