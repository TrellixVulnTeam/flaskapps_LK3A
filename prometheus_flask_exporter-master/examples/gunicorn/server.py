from flask import Flask

from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

app = Flask(__name__)
metrics = GunicornPrometheusMetrics(app)


@app.route('/test')
def index():
    return 'Hello world'


if __name__ == '__main__':
    app.run(debug=False, port=5000)
