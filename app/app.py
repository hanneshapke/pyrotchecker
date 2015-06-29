import os
from flask import (
    Flask, request, render_template, jsonify)
from werkzeug.contrib.fixers import ProxyFix
from rotchecker import ROTCypher

app = Flask(__name__)


##################################################################
# Routes:
# / - index page with static searcgh site
# /api - api interface with rot-search functionality
# /api/<int:n shift> - api interface with rot-search
#                      functionality for a give shift of n letters
##################################################################


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/', methods=['GET'])
@app.route('/api/<int:rot_shift>/', methods=['GET'])
def rot_check(rot_shift=13):
    cypher = ROTCypher(rot_shift)
    cypher.check_website_for_rot(
        request.args.get('url'),
        request.args.get('q'),
        request.args.get('t'),)
    response = jsonify(
        message=cypher.message,
        status=cypher.status)
    return response

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
