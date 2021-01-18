from flask import Flask, jsonify
from flask_migrate import Migrate
from models import setup_db,Plant,db
from flask_cors import CORS

app = Flask(__name__)
Migrate(app,db)
setup_db(app)
CORS(app)

# CORS Headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow_Headers','Content-Type,Authorization')
    response.headers.add('Access-Controll-Allow-Methods','POST,PATCH,DELETE,GET,OPTIONS')
    return response

@app.route('/')
def index():
    return jsonify({'name':'Nuwan'})

@app.route('/messages')
#@cross_origin()
def get_messages():
    return jsonify({'name':'Nuwan11111111111111111'})

if __name__ == "__main__":
    app.run()