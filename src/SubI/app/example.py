#!/home/cristina/Documentos/tfg.cristinabolanos/src/SubI/bin/python

from flask import Flask, url_for, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return 'index'

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		return 'logueado'
	else:
		return 'login'

@app.route('/user/<username>')
def profile(username):
	return '{}\'s profile'.format(username)

with app.test_request_context():
	print(url_for('index'))
	print(url_for('login'))
	print(url_for('profile', username='John Doe'))
