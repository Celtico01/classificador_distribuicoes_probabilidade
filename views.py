from flask import render_template
from app import app

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/v1/classificar/')
def classificar():
    pass

@app.route('/api/v1/resultado/')
def resultado():
    pass