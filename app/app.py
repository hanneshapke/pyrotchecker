from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/', methods=['GET'])
@app.route('/api/<int:rot_shift>', methods=['GET'])
def rot_check(rot_shift=13):
    return ('Hello World! > Shift is %s' % request.args.get('url'))


if __name__ == '__main__':
    app.run(debug=True)
