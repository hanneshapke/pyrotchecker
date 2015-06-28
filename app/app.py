from flask import Flask, request, render_template
app = Flask(__name__)

from rotchecker import ROTCypher


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/', methods=['GET'])
@app.route('/api/<int:rot_shift>', methods=['GET'])
def rot_check(rot_shift=13):
    cypher = ROTCypher(rot_shift)
    test = cypher.check_website_for_rot(request.args.get('url'), [request.args.get('q'), ])
    return ('Hello World! > Shift is %s' % test)


if __name__ == '__main__':
    app.run(debug=True)
