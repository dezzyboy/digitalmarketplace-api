from flask import jsonify

from .main import main
from .callbacks import callbacks
from .models import ValidationError


@main.app_errorhandler(ValidationError)
@callbacks.app_errorhandler(ValidationError)
def validation_error(e):
    return jsonify(error=e.message), 400


def generic_error_handler(e):
    headers = []
    code = getattr(e, 'code', 500)
    error = getattr(e, 'description', 'Internal error')

    if code == 401:
        headers = [('WWW-Authenticate', 'Bearer')]
    elif code == 500:
        error = "Internal error"

    return jsonify(error=error), code, headers


for code in range(400, 599):
    main.app_errorhandler(code)(generic_error_handler)
    callbacks.app_errorhandler(code)(generic_error_handler)
