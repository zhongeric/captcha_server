from flask import Flask, request, jsonify, render_template, redirect
import logging
import _thread
from datetime import datetime
from time import sleep
import webbrowser
import json


tokens = []
s = '6LeWwRkUAAAAAOBsau7KpuC9AV-6J8mhw4AjC3Xz'
d = 'supremenewyork.com'


def manageTokens():
	while True:
		for token in tokens:
			if token['expiry'] < datetime.now().timestamp():
				tokens.remove(token)
				print("Token expired and deleted.")
		sleep(5)


def sendToken():
	while not tokens:
		pass
	token = tokens.pop(0)
	return token['token']


app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def home():
	return render_template('i.html', sitekey=s, domain=d)

@app.route('/submit', methods=['POST'])
def submit():
	token = request.form['g-recaptcha-response']
	expiry = datetime.now().timestamp() + 115
	tokenDict = {
		'token': token,
		'expiry': expiry
	}
	tokens.append(tokenDict)
	print("Token harvested and stored.", "green")
	return redirect('/')

@app.route('/count')
def count():
	count = len(tokens)
	return jsonify(count=count)

@app.route('/token')
def fetch_token():
	try:
		token = tokens.pop(0)
		print("Token requested and returned to user.")
		return token['token']
	except:
		print("Token requested but none available.")
		return "ERROR"


if __name__ == '__main__':
	_thread.start_new_thread(manageTokens, ())
	app.run()
