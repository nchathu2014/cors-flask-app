from flask import Flask, jsonify
from flask-cors import CORS

app = Flask(__name__)


# CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

@app.route('/')
def index():
    return jsonify({name:'Nuwan'})

@app.route('/messages')
@cross_origin()
def get_messages():
    return 'GETTING_MESSAGES'

if __name__ == "__main__":
    app.run()