# start flask web serve
import flask

app = flask.Flask(__name__)

# serve files from folder static


@app.route('/<path:path>')
def send_js(path):
    return flask.send_from_directory('static', path)

# serve index.html


@app.route('/')
def send_index():
    return flask.send_from_directory('static', 'index.html')


if __name__ == '__main__':
    # run on port 8080
    app.run(host='0.0.0.0', port=8080)

