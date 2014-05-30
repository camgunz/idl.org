from idl import app

class BaseCache(object):

    def __init__(self):
        self.disabled = False
        try:
            self.test()
        except:
            self.disabled = True
            if app.config['DEBUG']:
                raise

    def generate_key(self, *args):
        return '.'.join([str(x).replace(' ', '_') for x in args])

    def test(self):
        raise NotImplementedError()

    def get_connection(self):
        raise NotImplementedError()

    def get(self, key):
        raise NotImplementedError()

    def set(self, key, value):
        raise NotImplementedError()

    def delete(self, key):
        raise NotImplementedError()

