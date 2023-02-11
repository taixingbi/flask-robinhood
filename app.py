import json
from flask import Flask
from flask import make_response

from robin.robintrade import robintrade

def jsonify(status=200, indent=4, sort_keys=True, **kwargs):
    response = make_response(json.dumps(dict(**kwargs), indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response

app = Flask(__name__)
@app.route('/')
def index():

    Robintrade = robintrade(quantity=1)
    Robintrade.cancelAllOrders()
    rs = Robintrade.straddle(order = True)
    return jsonify(indent=2, sort_keys=False, flask_response=rs)

    return json.dumps(rs, indent=2)
    return json.dumps({'name': 'robinhood',
                       'key': 'straddle'})


if __name__ == '__main__':
    app.run(host='0.0.0.0')


