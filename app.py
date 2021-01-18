from flask import Flask, jsonify,request
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

@app.route('/plants',methods=['GET'])
def get_all_plants():
    # #adding pagination
    page = request.args.get('page',1,type=int)  # if arg object page not found assign default to 1
    start = (page-1)*10
    end = start +10

    plants = Plant.query.all()
    formatted_plants = [plant.format() for plant in plants]
    print(plants)
    return jsonify({
        'plants':formatted_plants[start:end],
        'total_plants':len(formatted_plants),
        'success':True
    })

if __name__ == "__main__":
    app.run()