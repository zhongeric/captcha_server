class headerMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print('Function called')
        environ['HTTP_HOST'] = 'www.supremenewyork.com'
        environ['REMOTE_ADDR'] = 'www.supremenewyork.com'
        environ['SERVER_NAME'] = 'www.supremenewyork.com'
        print(environ)
        return self.app(environ, start_response)
