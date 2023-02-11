import json
from flask import Flask

from credential import rbCredential

app = Flask(__name__)
@app.route('/')
def index():
    rs = rbCredential().login()
    return json.dumps({'name': 'robinhood',
                       'key': 'straddle'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')


