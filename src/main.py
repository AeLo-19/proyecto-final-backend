"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for, make_response
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

                new_paciente = Paciente(new_user_data["name"], new_user_data["lastname"], new_user_data["email"], new_user_data["phone"], new_user_data["cedula"], new_user_data["password"])

                if new_paciente.set_birth_date(new_user_data["dateOfBirth"]):
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

@app.route("/register/doctor", methods=["POST"])
def handle_register_doctor():
    headers = {
        "Content-Type": "application/json"
    }
    # creating_user = Paciente.query.filter_by(email=email, cedula=cedula).all()
    if request.json:

        new_doctor_data = request.json

        if set(("dr_name", "dr_lastname", "dr_email", "dr_password", "dr_date_of_birth", "dr_phone", "dr_cedula", "certificado")).issubset(new_doctor_data):

            if validate_email_syntax(new_doctor_data["dr_email"]):

                new_doctor = Doctor(new_doctor_data["dr_name"], new_doctor_data["dr_lastname"], new_doctor_data["dr_email"], new_doctor_data["dr_phone"], new_doctor_data["dr_cedula"], new_doctor_data["dr_password"], new_doctor_data["certificado"])

                if new_doctor.set_birth_date(new_doctor_data["dr_date_of_birth"]):
                    db.session.add(new_doctor)
                    try:
                        db.session.commit()
                        status_code = 201
                        result = f"{new_doctor.name} has sido registrado de forma efectiva con el correo {new_doctor.email}"
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
                    if new_user_data["dr_password"]:
                        response_body = {
                            "result": "HTTP_400_BAD_REQUEST. Check your date of birth"
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
        status_code = 400
        response_body = {
            "result": "HTTP_400_BAD_REQUEST. no json data to register"
        }
    return make_response (
        json.dumps(response_body),
        status_code,
        headers
    )
@app.route("/citas", methods=["GET"])
@app.route("/user/<user_id>/citas", methods=["GET", "POST"])
@app.route("/user/<user_id>/citas/<cita_id>", methods=["POST", "GET", "PUT"])
def handle_cita(user_id=None, cita_id=None):
    headers = {
        "Content-Type": "application/json"
    }
    if request.method == "POST":
        new_cita_data = request.json
        if set(("date", "state", "tratamiento_value")).issubset(new_cita_data):

            new_cita_paciente_id = user_id
            new_cita_date = new_cita_data["date"]
            new_cita_state = new_cita_data["state"]
            new_cita_tratamiento = new_cita_data["tratamiento_value"]
            print(f"este es tratamiento: {type(new_cita_tratamiento)}")
            if (len(new_cita_date) > 0 and new_cita_tratamiento > 0):
                new_cita = Cita(new_cita_paciente_id, new_cita_date, new_cita_state, new_cita_tratamiento)

                db.session.add(new_cita)
                try:
                    db.session.commit()
                    status_code = 201
                    result = f"HTTP_201_CREATED. Cita creada efectivamente con el id {new_cita.id}"
                    response_body = {
                        "result": result
                    }
                except:
                    db.session.rollback()
                    status_code = 500
                    response_body = {
                        "result": "Algo ha salido mal."
                    }
            else:
                status_code = 400
                response_body = {
                    "result": "HTTP_400_BAD_REQUEST. some value empty"
                    }
        else:
            status_code = 400
            response_body = {
                "resultado": "HTTP_400_BAD_REQUEST. some key is empty"
            }
    elif request.method == "GET":
        if user_id:
            specific_user_citas = Cita.query.filter_by(paciente_id=user_id).all()
            response_body = []
            for cita in specific_user_citas:
                response_body.append(cita.serialize())
        elif cita_id:
            specific_user_and_cita = Cita.query.filter_by(paciente_id=user_id, id=cita_id).one_or_none()
            response_body = []
            for cita in specific_user_and_cita:
                response_body.append(cita.serialize())
        else:
            users_citas = Cita.query.filter_by(state=False).all()
            response_body = []
            for cita in users_citas:
                response_body.append(cita.serialize())
        
        status_code = 200 
    elif request.method == "PUT":
    
        edit_cita_data = request.json

        
        if set(("date", "state", "tratamiento_value")).issubset(edit_cita_data):
            print("entré aquí")  
            if cita_id:
                cita_to_edit = Cita.query.filter_by(id=cita_id).all()
                if cita_to_edit:
                    cita_to_edit.update(edit_cita_data)
                    try:
                        db.session.commit()
                        status_code = 200
                        response_body = {
                            "result": "HTTP_200_OK. La cita ha sido actualizada"
                        }
                    except: 
                        status_code = 400
                        response_body = {
                            "result": "HTTP_400_BAD_REQUEST.  No estoy funcionando"
                        }
                else: 
                    status_code = 404
                    response_body = {
                        "result": "HTTP_404_NOT_FOUND. no existe esa cita..."
                    }
            else:
                status_code = 500
                response_body = {
                    "result": "HTTP_500_INTERNAL_SERVER_ERROR. cita_id is not in the url"
                }
        else:
            status_code = 400
            response_body = {
                "result": "HTTP_BAD_REQUEST. data input invalid for cita update"
            }

    else:
        status_code = 400
        response_body = {
            "result": "HTTP_400_BAD_REQUEST. no json data to register"
        }
    return make_response (
        json.dumps(response_body),
        status_code,
        headers
    )


@app.route("/tratamiento", methods=["POST", "GET"])
def handle_tratamiento():
    headers ={
        "Content-Type": "application/json"
    }
    if request.method == "POST":
        new_tratamiento_data = request.json

        if set(("tratamiento_name", "descripcion", "price")).issubset(new_tratamiento_data):
            new_tratamiento_name = new_tratamiento_data["tratamiento_name"]
            new_tratamiento_descripcion = new_tratamiento_data["descripcion"]
            new_tratamiento_price = new_tratamiento_data["price"]
            if(len(new_tratamiento_name) > 0 and len(new_tratamiento_descripcion) > 0 and len(new_tratamiento_price) > 0):
                new_tratamiento = Tratamiento(new_tratamiento_name, new_tratamiento_descripcion, new_tratamiento_price)

                db.session.add(new_tratamiento)
                try:

                    db.session.commit()
                    status_code = 201
                    result = f"HTTP_201_CREATED.el  tratamiento ha sido guardado de forma efectiva con el siguiente id: {new_tratamiento.id}"
                    response_body = {
                    "result": result
                    }
                except:
                    db.session.rollback()
                    status_code = 500
                    response_body = {
                        "result": "algo salió mal"
                    }
            else:
                status_code = 400
                response_body = {
                    "result": "HTTP_400_BAD_REQUEST. Algun input se encuentra vacío"
                }

    elif request.method == "GET":
        tratamientos = Tratamiento.query.all()
        response_body = []
        for tratamiento in tratamientos:
            response_body.append(tratamiento.serialize())
        status_code = 200 

    else: 
        status_code = 400
        response_body = {
            "result": "HTTP_400_BAD_REQUEST. no json data to register"
        }
    return make_response(
        json.dumps(response_body),
        status_code,
        headers
    )




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
