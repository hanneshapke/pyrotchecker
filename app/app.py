from flask import Flask, request, render_template, jsonify
app = Flask(__name__)

from rotchecker import ROTCypher

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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
