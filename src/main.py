"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap, validate_email_syntax
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

@app.route("/register", methods=["POST"])
def handle_register():
    headers = {
        "Content-Type": "application/json"
    }
    # creating_user = Paciente.query.filter_by(email=email, cedula=cedula).all()
    if request.json:

        new_user_data = request.json

        if set(("name", "lastname", "email", "password", "dateOfBirth", "phone", "cedula")).issubset(new_user_data):

            if validate_email_syntax(new_user_data["email"]):

                new_paciente = Paciente(new_user_data["name"], new_user_data["lastname"], new_user_data["email"], new_user_data["phone"], new_user_data["cedula"])

                if new_paciente.set_birth_date(new_user_data["dateOfBirth"]) and new_user_data["password"]:
                    new_paciente.set_password(new_user_data["password"])
                    db.session.add(new_paciente)
                    try:
                        db.session.commit()
                        status_code = 201
                        result = f"{new_paciente.name} has sido registrado de forma efectiva con el correo {new_paciente.email}"
                        response_body = {
                            "result": result
                        }
                    except IntegrityError:
                        db.session.rollback()
                        status_code = 400
                        result = "HTTP_400_BAD_REQUEST. The email is taken"
                        response_body = {
                            "result": result
                        }
                else:
                    status_code = 400
                    if new_user_data["password"]:
                        response_body = {
                            "result": "HTTP_400_BAD_REQUEST. Check your sate of birth"
                        }
                    else:
                        response_body = {
                            "result": "HTTP_400_BAD_REQUEST. Password is empty"
                        }
            else:
                status_code = 400
                response_body = {
                    "result": "HTTP_400_BAD_REQUEST. Check the email"
                }
        else:
            status_code = 400
            response_body = {
                "result": "HTTP_400_BAD_REQUEST. check your input"
            }
    else:
        tatus_code = 400
        response_body = {
            "result": "HTTP_400_BAD_REQUEST. no json data to register"
        }
    return make_response (
        json.dumps(response_body),
        status_code,
        headers
    )

    
    # if len(creating_user) > 0:
    #     user_id = creating_user[0].id
    # else : 
    #     user_id = None

    # if request.method == 'POST':

    #     print("Iniciando el POST de registro")

    #     if user_id:

    #         response_body = {
    #             "status": "HTTP_400_BAD_REQUEST. Ya existe ese usuario"
    #         }
    #         status_code = 400
        
    #     if:
    #         print("Creando usuario")
    #         user_data = request.json
    #         new_user = Paciente(user_data["name"], user_data["lastname"] user_data["email"], user_data["password"], user_data["date_of_birth"], user_data["phone"], user_data["cedula"])
    #         db.session.add(new_user)
    #         db.session.commit()
    #         response_body = {
    #             "status": "todo ok"
    #         }
    #         status_code = 200
    # return make_response(
    #     jsonify(response_body),
    #     status_code,
    #     headers
    # )



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
