from flask import jsonify, make_response
from werkzeug.http import HTTP_STATUS_CODES


def gen_error(error, status_code, status=None, msg=None):
    message = str(error) or msg
    res = jsonify(status, {"msg": f"{HTTP_STATUS_CODES[status_code]}. {message}"})
    return make_response(res, status_code)

def handle_500_error(error):
    return gen_error(error, 500, "Server error")

def handle_404_error(error):
    return gen_error(error, 404, "error" if isinstance(error, KeyError) else "fail")

def handle_400_error(error):
    return gen_error(error, 400, "error")