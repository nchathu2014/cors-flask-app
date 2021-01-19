from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from models import setup_db, Plant, db, paginate_plants
from flask_cors import CORS

app = Flask(__name__)
Migrate(app, db)
setup_db(app)
CORS(app)

# CORS Headers


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow_Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Controll-Allow-Methods',
                         'POST,PATCH,DELETE,GET,OPTIONS')
    return response

# GET


@app.route('/plants', methods=['GET'])
def get_all_plants():

    plants = Plant.query.order_by(Plant.id).all()
    current_plants = paginate_plants(request, plants)

    if len(current_plants) == 0:
        abort(404)

    return jsonify({
        'plants': current_plants,
        'total_plants': len(plants),
        'success': True
    })


@app.route('/plants/<int:plant_id>')
def get_speific_plant(plant_id):

    #plant = Plant.query.get(plant_id)
    #plant = Plant.query.filter_by(id=plant_id).one_or_none()
    plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

    if plant is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'plant': plant.format()
        })


# PATCH
@app.route('/plants/<int:plant_id>', methods=['PATCH'])
def update_book(plant_id):
    body = request.get_json()

    try:
        plant = Plant.query.get(plant_id)

        if plant is None:
            abort(404)

        if 'name' in body:
            plant.name = body['name']

        plant.update()

        return jsonify({
            'success': True
        })

    except:
        abort(404)

# DELETE


@app.route('/plants/<int:plant_id>', methods=['DELETE'])
def delete_specific_plant(plant_id):

    try:
        plant = Plant.query.get(plant_id)
        if plant is None:
            abort(404)

        plant.delete()
        plants = Plant.query.order_by(Plant.id).all()
        current_plants = paginate_plants(request, plants)
        return jsonify({
            'success': True,
            'deleted': plant_id,
            'plants': current_plants,
            'total_plants': len(Plant.query.all())
        })
    except:
        abort(422)

# CREATE


@app.route('/plants', methods=['POST'])
def create_new_plant():
    body = request.get_json()

    name = body["name"]
    scientific_name = body["scientific_name"]
    is_poisonous = body["is_poisonous"]
    primary_color = body["primary_color"]

    try:
        new_plant = Plant(name=name, scientific_name=scientific_name,
                          is_poisonous=is_poisonous, primary_color=primary_color)
        new_plant.insert()
        plants = Plant.query.order_by(Plant.id).all()
        current_plants = paginate_plants(request, plants)

        return jsonify({
            "success": True,
            "created": new_plant.id,
            "plants": current_plants,
            "total_plants": len(plants)
        })
    except:
        abort(422)

# Error Handling


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(405)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


if __name__ == "__main__":
    app.run()
