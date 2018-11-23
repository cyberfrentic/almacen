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


class inventario(db.Model):
	__tablename__ = 'inventario'
	id_item = db.Column(db.String(20), primary_key=True, comment='codigo producto')
	id_prod = db.Column(db.String(20))
	tipo_prod = db.Column(db.String(20))
	nom_prod = db.Column(db.String(255))
	nom_interno = db.Column(db.String(255))
	descripcion = db.Column(db.String(255))
	um = db.Column(db.String(20))
	id_area = db.Column(db.String(20))
	f_alta = db.Column(db.DateTime, default=datetime.datetime.now) #auntomatico
	ultim_modif = db.Column(db.DateTime, onupdate=datetime.datetime.now) #automatico
	activo = db.Column(db.Boolean)
	id_familia = db.Column(db.String(20))
	procedencia = db.Column(db.String(255))
	modelo = db.Column(db.String(50))
	num_parte = db.Column(db.String(30))
	num_serie = db.Column(db.String(30))
	id_proveed = db.Column(db.String(20))
	f_recepcion = db.Column(db.DateTime)
	f_fabricacion = db.Column(db.Date)
	f_caducidad = db.Column(db.Date)
	cant_exist = db.Column(db.Numeric(18,6))
	cant_dispon = db.Column(db.Numeric(18,6))
	costo_unit = db.Column(db.Numeric(18,6))
	moneda = db.Column(db.String(10))
	id_area_soli = db.Column(db.String(20))
	folio_entrada = db.Column(db.String(30))
	folio_salida = db.Column(db.String(30))
	folio_e_s = db.Column(db.String(30))
	solic_tansfer = db.Column(db.String(30))
	observaciones = db.Column(db.String(50))
	orden_compra = db.Column(db.String(50))
	num_requerim = db.Column(db.String(50))
	factura_nota = db.Column(db.String(50))
	f_salida = db.Column(db.DateTime)
	tipo_compra = db.Column(db.String(30))
	actividad = db.Column(db.String(100))
	num_oper = db.Column(db.Integer)

	def __init__(self, id_item, id_prod, tipo_prod, nom_prod, nom_interno, descripcion, um, id_area, activo, id_familia, procedencia,
	 modelo, num_parte, num_serie, id_proveed, f_recepcion, f_fabricacion, f_caducidad, cant_exist, cant_dispon, costo_unit, moneda,
	  id_area_soli, folio_entrada, folio_salida, folio_e_s, solic_tansfer, observaciones, orden_compra, num_requerim, factura_nota, 
	  f_salida, tipo_compra, actividad,num_oper):
		self.id_item = id_item
		self.id_prod = id_prod
		self.tipo_prod = tipo_prod
		self.nom_prod = nom_prod
		self.nom_interno = nom_interno
		self.descripcion = descripcion
		self.um = um
		self.id_area = id_area
		self.activo = activo
		self.id_familia = id_familia
		self.procedencia = procedencia
		self.modelo = modelo
		self.num_parte = num_parte
		self.num_serie = num_serie
		self.id_proveed = id_proveed
		self.f_recepcion = f_recepcion
		self.f_fabricacion = f_fabricacion
		self.f_caducidad = f_caducidad
		self.cant_exist = cant_exist
		self.cant_dispon = cant_dispon
		self.costo_unit = costo_unit
		self.moneda = moneda
		self.id_area_soli = id_area_soli
		self.folio_entrada = folio_entrada
		self.folio_salida = folio_salida
		self.folio_e_s =folio_e_s
		self.solic_tansfer = solic_tansfer
		self.observaciones = observaciones
		self.orden_compra = orden_compra
		self.num_requerim = num_requerim
		self.factura_nota = factura_nota
		self.f_salida = f_salida
		self.tipo_compra = tipo_compra
		self.actividad = actividad
		self.num_oper = num_oper