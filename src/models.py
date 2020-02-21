from flask_sqlalchemy import SQLAlchemy
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from utils import parse_time_of_day
from datetime import datetime, time
import json
db = SQLAlchemy()

class User(db.Model):
    __abstract__=True
    name = db.Column(db.String(80), unique=False, nullable=False)
    lastname = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(150), unique=False, nullable=False)
    date_of_birth = db.Column(db.Date, unique=False, nullable=False)
    cedula = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(80), unique=True, nullable=False)
    
    def set_birth_date(self, date):
        try:
            self.date_of_birth = parse(date)
            # enforce age rules for user object creation
            if self.date_of_birth <= datetime.now() - relativedelta(years=18):
                return True
            else:
                return False
        except ValueError:
            return False
        
    # def __repr__(self):
    #     return  '<User %r>' % self.username
    
    # def __hash__(self):
    #     return hash((self.password, self.phone))

    
    
class Paciente(User) :
    __tablename_ = 'paciente'
    id = db.Column(db.Integer, primary_key=True)
    citas = db.relationship('Cita', backref='paciente', lazy=True)

    def __init__(self, name, lastname, email, phone, cedula, password):
        self.name = name.strip()
        self.lastname = lastname.strip()
        self.email = email.strip()
        self.password = password.strip()
        self.phone = phone.strip()
        self.cedula = cedula.strip()
        


class Doctor(User):
    __tablename_ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    certificado = db.Column(db.String(250), unique=False, nullable=False)
    # citas = db.relationship('Cita', backref='doctor', lazy=True)

    def __init__(self, name, lastname, email, phone, cedula, password, certificado):
        self.name = name.strip()
        self.lastname = lastname.strip()
        self.email = email.strip()
        self.phone = phone.strip()
        self.cedula = cedula.strip()
        self.password = password.strip()
        self.certificado = certificado.strip()

class Cita(db.Model):
    __tablename__ = "cita"
    id = db.Column(db.Integer, primary_key=True)
    planned_date = db.Column(db.Date, unique=False, nullable=False)
    state = db.Column(db.Boolean)
    # price_tot = db.Column(db.Integer, unique=False, nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    # doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    tratamiento_id = db.Column(db.Integer, db.ForeignKey("tratamiento.id"))

    def __init__(self, paciente_id, planned_date, state, tratamiento_id):
        self.paciente_id = paciente_id.strip()
        self.state = json.loads(state)
        self.planned_date = datetime.strptime(planned_date, "%Y/%m/%d")
        self.tratamiento_id = tratamiento_id
    
    def serialize(self):
        return{
            "id": self.id,
            "plannedDate": self.planned_date.isoformat(),
            "state": self.state,
            "pacienteId": self.paciente_id,
            "tratamientoId": self.tratamiento_id
        }

    def update(self, json_data):
        self.state = bool(json_data["state"])
        self.planned_date = json_data["date"]
        self.tratamiento_id = json_data["tratamiento_value"]
        #.strptime(planned_date, "%Y/%m/%d")

class Tratamiento(db.Model):
    __tablename__ = 'tratamiento'
    id = db.Column(db.Integer, primary_key=True)
    tratamiento_name = db.Column(db.String(125), unique=True, nullable=False)
    descripcion = db.Column(db.String(500), unique=True, nullable=True)
    price = db.Column(db.String(200), unique=False, nullable=False)
    citas = db.relationship("Cita", backref="tratamiento")   

    def __init__(self, tratamiento_name, descripcion, price):
        self.tratamiento_name = tratamiento_name.strip()
        self.descripcion = descripcion.strip()
        self.price = price.strip()
#serialize
    def serialize(self):
        return{
            "id": self.id,
            "tratamientoName": self.tratamiento_name,
            "descripcion": self.descripcion,
            "price": self.price,
        }
    


# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<Person %r>' % self.username

#     def serialize(self):
#         return {
#             "username": self.username,
#             "email": self.email
#         }