from main import app
from flask import send_from_directory

import constants

if constants.DEBUG:
    @app.route('/swagger.yml', methods=['GET'])
    def swagger():
        return send_from_directory(constants.BASE_DIR, 'swagger.yml')

