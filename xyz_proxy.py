import requests
from robosat_pink.geoc import config as CONFIG
from flask import Flask, request, Response
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello flask!'


@app.route('/v1/wmts/<z>/<x>/<y>', methods=['GET'])
def wmts(x, y, z):
    map = request.args.get("type")
    if not x or not y or not z:
        return None
    if not map and map != "tdt" and map != "google":
        return "faild to set map type, neither tianditu nor google"
    url = CONFIG.URL_TDT
    url_google = CONFIG.URL_GOOGLE
    if map == 'google':
        url = url_google
    image = requests.get(url.format(x=x, y=y, z=z))

    print(url.format(x=x, y=y, z=z))
    return Response(image, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(port=CONFIG.FLASK_PORT)

# How to run this server backend?
# >: python xyz_proxy.py &
