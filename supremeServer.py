from flask import Flask, render_template, request
from threading import Thread
from sys import argv
import logging, time, sys

logging.getLogger('werkzeug').setLevel(logging.ERROR)

tokens = {'tokens':[],'used':[]}
success_list = []
counter = 0

app = Flask(__name__)

def tokenremoval(token):
    tokens['tokens'].append(token)
    time.sleep(110)
    tokens['tokens'].remove(token)

    
@app.route("/", methods=['GET'])
def main():
    return render_template('supreme.html')

@app.route("/success", methods=['GET','POST'])
def success():
    if request.method == "POST":
        #counter + 1
        timestamp = request.form.get('timestamp', '')
        product = request.form.get('product-title', '')
        string_formatted = 'Product Success ' + str(product) + ' [' + str(timestamp) + ']'
        success_list.append(string_formatted)
        #return(success_list)
    if request.method == "GET":
        return(str(success_list))

@app.route('/json', methods=['GET'])
def json():
    content = tokens
    return(render_template('json.html', content = content))

@app.route('/solve', methods=['POST'])
def solve():
    if request.method == "POST":
        token = request.form.get('g-recaptcha-response', '')
        print('Posted Token : ' + token)
        Thread(target = tokenremoval, args = [token]).start()
    return('token=' + token)

@app.route('/used', methods=['POST'])
def used():
    token = request.form.get('usedtoken', '')
    print('Used Token : ' + token)
    tokens['used'].append(token)
    return('Success')

if __name__ == "__main__":
    app.run(host = '127.0.0.1', debug=True)
    #Thread(target = lambda: app.run(host = '0.0.0.0', ssl_context='adhoc', port=3500)).start()
