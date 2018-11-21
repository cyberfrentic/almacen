from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime

db = SQLAlchemy()


class User(db.Model):
	__tablename__= 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(40))
	password = db.Column(db.String(93))
	created_date = db.Column(db.DateTime, default=datetime.datetime.now)

	def __init__(self, username, password, email):
		self.username = username
		self.password = self.__crate_password(password)
		self.email = email

	def __crate_password(self, password):
		return generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password, password)

class Compras(db.Model):
	__tablename__='compras'
	id = db.Column(db.Integer, primary_key=True)
	UUiD = db.Column(db.String(36), unique=True)
	rfc = db.Column(db.String(13), index=True)
	nombre = db.Column(db.String(150))
	subtotal = db.Column(db.Float)
	iva = db.Column(db.Float)
	total = db.Column(db.Float)
	fecha = db.Column(db.DateTime)
	placas = db.Column(db.String(8))
	observaciones = db.Column(db.Text)
	folio = db.Column(db.Integer)


class Articulos(db.Model):
	__tablename__ = 'articulos'
	id = db.Column(db.Integer, primary_key=True)
	compras_id = db.Column(db.Integer, db.ForeignKey("compras.id"), nullable=False)
	compras = relationship(Compras, backref = backref('comprass', uselist=True))
	cantidad = db.Column(db.Float)
	descripcion = db.Column(db.String(150))
	p_u = db.Column(db.Float)
	importe = db.Column(db.Float)

class Padron(db.Model):
	__tablename__='padron'
	cuenta = db.Column(db.Integer, primary_key=True, unique=True, index=True)
	nombre = db.Column(db.String(120))
	direccion = db.Column(db.String(150))

