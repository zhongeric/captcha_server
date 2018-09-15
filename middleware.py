class headerMiddleware(object):

def __init__(self, app):
self.app = app

def __call__(self, environ, start_response):
 print(‘ — — — — — — — — — — -’)
 print(‘Function called’)
 print(‘ — — — — — — — — — — -’)
 environ['host'] = 'http://www.supremenewyork.com'
 return self.app(environ, start_response)
