import json
from flask import Flask

from credential import rbCredential


app = Flask(__name__)
@app.route('/')
def index():

    rs = rbCredential().login()



    return json.dumps({'name': 'robinhood',
                       'key': 'straddle'})
app.run()

