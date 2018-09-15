from flask import Flask, render_template, request, redirect
from threading import Thread
from sys import argv
import logging, time, sys
import unittest
import middleware

logging.getLogger('werkzeug').setLevel(logging.ERROR)

tokens = {'tokens':[],'used':[]}
success_list = []
counter = 0
domain = "http://www.supremenewyork.com/"
htmlcode = """
<html>
   <meta name='viewport' content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no'>
   <head>
      <script type='text/javascript' src='https://www.google.com/recaptcha/api.js'></script><script src='http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js' type='text/javascript'></script>
      <title>Captcha Harvester</title>
      <style type='text/css'> body{margin: 1em 5em 0 5em; font-family: sans-serif;}fieldset{display: inline; padding: 1em;}</style>
   </head>
   <body>
      <center>
         <h3>Captcha Token Harvester</h3>
         <h5>Please complete the captcha below.</h5>
         <form action='http://www.funkospace.us/solve' method='post'>
            <fieldset>
               <div class='g-recaptcha' data-sitekey='6LeWwRkUAAAAAOBsau7KpuC9AV-6J8mhw4AjC3Xz' data-callback='sub'></div>
               <p> <input type='submit' value='Submit' id='submit' style='color: #ffffff;background-color: #3c3c3c;border-color: #3c3c3c;display: inline-block;margin-bottom: 0;font-weight: normal;text-align: center;vertical-align: middle;-ms-touch-action: manipulation;touch-action: manipulation;cursor: pointer;background-image: none;border: 1px solid transparent;white-space: nowrap;padding: 8px 12px;font-size: 15px;line-height: 1.4;border-radius: 0;-webkit-user-select: none;-moz-user-select: none;-ms-user-select: none;user-select: none;'> </p>
            </fieldset>
         </form>
         <fieldset>
            <h5 style='width: 10vh;'> <a style='text-decoration: none;' href='http://www.funkospace.us/json' target='_blank'>Usable Tokens</a> </h5>
         </fieldset>
      </center>
      <script>function sub(){document.getElementById('submit').click();}</script>
   </body>
</html>
"""

app = Flask(__name__)
app.wsgi_app = middleware.headerMiddleware(app.wsgi_app)

h = {
    "Host":"www.supremenewyork.com"
}

def tokenremoval(token):
    tokens['tokens'].append(token)
    time.sleep(110)
    tokens['tokens'].remove(token)

@app.route("/supreme", methods=['GET'])
def supreme():
   return redirect("http://www.supremenewyork.com", code=302)
#     driver.get(domain)
#     try:
#         drive.execute_script('document.write("{}")'.format(htmlcode))
#     except selenium.common.exceptions.WebDriverException:
#         pass

@app.route("/now", methods=['GET'])
def now():
    print(request.headers)
    with app.test_request_context(headers=h):
        #return request.headers.get('host')
        return render_template('main.html'), {'Host': 'www.supremenewyork.com'}


@app.route("/", methods=['GET'])
def main():
    print(request.headers)
    return render_template('main.html')

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
    app.run(host = '0.0.0.0', debug=True)
    #Thread(target = lambda: app.run(host = '0.0.0.0', ssl_context='adhoc', port=3500)).start()


