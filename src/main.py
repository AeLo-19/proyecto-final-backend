"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, User, Paciente, Doctor, Cita, Tratamiento
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

@app.route("/login", methods=["POST"])
def handle_login(email, password):
    headers = {
        "Content-Type": "application/json"
    }
    requesting_login_paciente = Paciente.query.filter_by(email=email, password=password).all()
    requesting_login_doctor = Doctor.query.filter_by(email=email, password=password).all()
    if request.method == "POST":
        print("Hola estoy empezando a hacer la consulta!")
        if len(requesting_login_doctor) > 0:
            print("El perfil si existe! puede seguir")
            response_body = {
                "status": "HTTP_200_OK. Adelante."
            }
            status_code = 200
        elif len(requesting_login_paciente) > 0:
            print("El perfil si existe! puede seguir")
            response_body = {
                "status": "HTTP_200_OK. Adelante."
            }
            status_code = 200
        else:
            print("El perfil no existe por favor revise los datos")
            response_body={
                "status": "HTTP_404_NOT_FOUND. El perfil no se encuantra registrado"
            }
            status_code = 400


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
