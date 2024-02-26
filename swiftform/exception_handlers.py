from flask import jsonify

def on_exception(e):
    return jsonify({"message": str(e)}), 500

class ExceptionHandlers(object):
    def init_app(self, app):
        app.register_error_handler(Exception, on_exception)
