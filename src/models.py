from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __abstract__=True
    name = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    age = db.Column(db.Date, unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return  '<User %r>' % self.username
    
    def __hash__(self):
        return hash((self.password, self.phone))
    
    

class Paciente(db.User):
    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.Integer, unique=True, nullable=False)

class Doctor(db.User):
    id = db.Column(db.Integer, primary_key=True)
    certificado = db.Column(db.String(250), unique=False, nullable=False)

class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=False, nullable=False)
    state = db.Column(db.Boolean)
    price_tot = db.Column(db.Integer, unique=False, nullable=False)

class Tratamiento(db.Column):
    id = db.Column(db.Integer, primary_key=True)
    tratamiento_name = db.Column(db.String(125), unique=True, nullable=False)
    descripcion = db.Column(db.String(250), unique=True, nullable=True)
    price = db.Column(db.int, unique=False, nullable=False)

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