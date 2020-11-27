from datetime import datetime
from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    time = datetime.now().ctime()
    return f'Time in Minsk: {time}'
