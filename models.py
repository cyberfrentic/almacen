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


class Inventario(db.Model):
	__tablename__ = 'inventario'
	id = db.Column(db.Integer, primary_key=True, comment='Id de control primary Key')
	id_item = db.Column(db.String(20), comment='codigo producto')
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
	f_recepcion = db.Column(db.DateTime, default=datetime.datetime.now)
	f_fabricacion = db.Column(db.Date, default=datetime.datetime.now)
	f_caducidad = db.Column(db.Date, default=datetime.datetime.now)
	cant_exist = db.Column(db.Numeric(18,6))
	cant_dispon = db.Column(db.Numeric(18,6))
	costo_unit = db.Column(db.Numeric(18,6))
	moneda = db.Column(db.String(10))
	id_area_solici = db.Column(db.String(20))
	solic_transfer = db.Column(db.String(30))
	observaciones = db.Column(db.String(150))
	usuario =  db.Column(db.String(250))
	fol_entrada = db.Column(db.String(30))
	fol_salida = db.Column(db.String(30))
	oficio_e_s = db.Column(db.String(30))
	id_proveed = db.Column(db.String(20))
	orden_compra = db.Column(db.String(50))
	num_requerim = db.Column(db.String(20))
	n_fact_nota = db.Column(db.String(30))
	f_salida = db.Column(db.DateTime)
	tipo_compra = db.Column(db.String(30))
	actividad = db.Column(db.String(30))

	def __init__(self,id,id_item, id_prod,tipo_prod,	nom_prod,nom_interno,descripcion,um,id_area,activo,
		id_familia,	procedencia, modelo, num_parte, num_serie,cant_exist,cant_dispon,
		costo_unit,	moneda,id_area_solici,solic_transfer,observaciones,usuario,	fol_entrada,	fol_salida,	oficio_e_s,	id_proveed,
		orden_compra,	num_requerim,	n_fact_nota,	f_salida,	tipo_compra,	actividad):
		self.id =id
		self.id_item =id_item
		self.id_prod =id_prod
		self.tipo_prod = tipo_prod
		self.nom_prod = nom_prod
		self.nom_interno = nom_interno
		self.descripcion =descripcion
		self.um =um
		self.id_area = id_area
		#self.f_alta = f_alta
		#self.ultim_modif = ultim_modif
		self.activo = activo
		self.id_familia = id_familia
		self.procedencia = procedencia
		self.modelo = modelo
		self.num_parte = num_parte
		self.num_serie = num_serie
		#self.f_recepcion = f_recepcion
		#self.f_fabricacion = f_fabricacion
		#self.f_caducidad = f_caducidad
		self.cant_exist = cant_exist
		self.cant_dispon = cant_dispon 
		self.costo_unit = costo_unit
		self.moneda = moneda
		self.id_area_solici  = id_area_solici
		self.solic_transfer = solic_transfer
		self.observaciones = observaciones
		self.usuario = usuario
		self.fol_entrada = fol_entrada
		self.fol_salida = fol_salida
		self.oficio_e_s = oficio_e_s
		self.id_proveed = id_proveed
		self.orden_compra = orden_compra
		self.num_requerim = num_requerim
		self.n_fact_nota = n_fact_nota
		self.f_salida = f_salida
		self.tipo_compra = tipo_compra
		self.actividad = actividad


class data_import_party(db.Model):
	group_name = db.Column(db.String(1000))
	group_name_local = db.Column(db.String(1000))
	external_id = db.Column(db.String(20), primary_key=True)
	parent_external_id = db.Column(db.String(20))
	nivel = db.Column(db.String(20))
	rol = db.Column(db.String(255))
	rfc = db.Column(db.String(255))
	moneda = db.Column(db.String(20))
	node = db.Column(db.String(1))
	state = db.Column(db.String(1))
	user_login_id = db.Column(db.String(250))
	import_status_id = db.Column(db.String(20))
	import_error = db.Column(db.String(8000))
	last_modifield_date = db.Column(db.DateTime,default=datetime.datetime.now)
	processed_timestamp =db.Column(db.DateTime,default=datetime.datetime.now)
	last_updated_stamp = db.Column(db.DateTime, default=datetime.datetime.now)
	last_updated_tx_stamp = db.Column(db.DateTime, default=datetime.datetime.now)
	created_stamp = db.Column(db.DateTime, default=datetime.datetime.now)
	created_tx_stamp =db.Column(db.DateTime, default=datetime.datetime.now)

	def __init__(self, group_name, group_name_local, external_id, parent_external_id, nivel, rol, rfc, moneda, node,
		state, user_login_id, import_status_id, import_error):
		self.group_name = group_name
		self.group_name_local = group_name_local
		self.external_id = external_id
		self.parent_external_id = parent_external_id
		self.nivel = nivel
		self.rol = rol
		self.rfc = rfc
		self.moneda = moneda
		self.node = node
		self.state = state
		self.user_login_id = user_login_id
		self.import_status_id = import_status_id
		self.import_error = import_error

	def __repr__(self):
		return '{}'.format(self.group_name_local)


class party_group(db.Model):
	party_id = db.Column(db.String(20), primary_key=True)
	group_name = db.Column(db.String(255))
	group_name_local = db.Column(db.String(255))
	federal_tax_id = db.Column(db.String(255))
	rfc = db.Column(db.String(20))
	regimen_id = db.Column(db.String(20))
	sector_economico_id = db.Column(db.String(20))
	origen_capital_id = db.Column(db.String(20))
	giro_empresa = db.Column(db.String(8000))
	nacional_extranjero = db.Column(db.String(60))
	correo_electronico = db.Column(db.String(60))
	pagina_web = db.Column(db.String(60))


	def __init__(self, party_id, group_name, group_name_local, federal_tax_id, rfc, regimen_id, sector_economico_id,
		origen_capital_id, giro_empresa, nacional_extranjero, correo_electronico, pagina_web):
		self.party_id = party_id
		self.group_name = group_name
		self.group_name_local = group_name_local
		self.federal_tax_id = federal_txt_id
		self.rfc = rfc
		self.regimen_id = regimen_id
		self.sector_economico_id = sector_economico_id
		self.origen_capital_id = origen_capital_id
		self.giro_empresa = giro_empresa
		self.nacional_extranjero = nacional_extranjero
		self.correo_electronico = correo_electronico
		self.pagina_web = pagina_web

	def __repr__(self):
		return '{}'.format(self.group_name)

class proveedor(db.Model):
	__tablename__= "proveedores"
	CONTACT_MECH_ID = db.Column(db.String(20), primary_key=True)
	TO_NAME = db.Column(db.String(100))
	ATTN_NAME = db.Column(db.String(100))
	ADDRESS1 = db.Column(db.String(255))
	ADDRESS2 = db.Column(db.String(255))
	DIRECTIONS = db.Column(db.String(255))
	CITY = db.Column(db.String(100))
	POSTAL_CODE = db.Column(db.String(60))
	LAST_UPDATED_STAMP = db.Column(db.DateTime, default=datetime.datetime.now)
	MUNICIPALITY_GEO_ID = db.Column(db.String(20))
	BANCO_ID = db.Column(db.String(20))
	NUMERO_CUENTA = db.Column(db.String(20))
	CLABE_INTERBANCARIA = db.Column(db.String(20))
	RFC = db.Column(db.String(20))

	def __init__(self, CONTACT_MECH_ID, TO_NAME, ATTN_NAME, ADDRESS1,ADDRESS2, DIRECTIONS, CITY, POSTAL_CODE, LAST_UPDATED_STAMP,
		MUNICIPALITY_GEO_ID, BANCO_ID, NUMERO_CUENTA, CLABE_INTERBANCARIA, RFC):
		self.CONTACT_MECH_ID = CONTACT_MECH_ID
		self.TO_NAME = TO_NAME
		self.ATTN_NAME = ATTN_NAME
		self.ADDRESS1 = ADDRESS1
		self.ADDRESS2 = ADDRESS2
		self.DIRECTIONS = DIRECTIONS
		self.CITY = CITY
		self.POSTAL_CODE = POSTAL_CODE
		self.LAST_UPDATED_STAMP = LAST_UPDATED_STAMP
		self.MUNICIPALITY_GEO_ID = MUNICIPALITY_GEO_ID
		self.BANCO_ID = BANCO_ID
		self.NUMERO_CUENTA = NUMERO_CUENTA
		self.CLABE_INTERBANCARIA = CLABE_INTERBANCARIA
		self.RFC = RFC

	def __repr__(self):
		return '{}'.format(self.TO_NAME)
		

class Entrada(db.Model):
	__tablename__ = "Entradas"
	id = db.Column(db.Integer, primary_key= True)
	proveedor = db.Column(db.String(255))
	nomComer = db.Column(db.String(255))
	fol_entrada = db.Column(db.String(30))
	fecha = db.Column(db.Date)
	factura = db.Column(db.String(2))
	nFactura = db.Column(db.String(15))
	ordenCompra = db.Column(db.String(15))
	depSolici = db.Column(db.String(150))
	nReq = db.Column(db.String(15))
	oSolicitnte = db.Column(db.String(60))
	tCompraContrato = db.Column(db.String(20))
	total = db.Column(db.Float)
	observaciones = db.Column(db.Text)

	def __init__(self, proveedor, nomComer, fol_entrada, fecha, factura, nFactura, ordenCompra, depSolici, nReq, oSolicitnte, tCompraContrato, total, observaciones):
		self.proveedor = proveedor
		self.nomComer = nomComer
		self.fol_entrada = fol_entrada
		self.fecha = fecha
		self.factura = factura
		self.nFactura = nFactura
		self.ordenCompra = ordenCompra
		self.depSolici = depSolici
		self.nReq = nReq
		self.oSolicitnte = oSolicitnte
		self.tCompraContrato = tCompraContrato
		self.total = total
		self.observaciones = observaciones


class Articulos(db.Model):
	__tablename__ = "entArti"
	id = db.Column(db.Integer, primary_key=True)
	entradas_id = db.Column(db.Integer)
	cantidad = db.Column(db.Float)
	udm = db.Column(db.String(15))
	codigo = db.Column(db.String(35))
	descripcion = db.Column(db.String(150))
	p_unit = db.Column(db.Float)
	total = db.Column(db.Float)
	ordenCompra = db.Column(db.String(15))
	imtemId = db.Column(db.Integer)

	def __init___(self, entradas_id, cantidad, udm, codigo, descripcion, p_unit, total, ordenCompra, imtemId):
		self.entradas_id = entradas_id
		self.cantidad = cantidad
		self.udm = udm
		self.codigo = codigo
		self.descripcion = descripcion
		self.p_unit = p_unit
		self.total = total
		self.ordenCompra = ordenCompra
		self.imtemId = imtemId


class Salidas(db.Model):
	__tablename__ = "salida"
	id = db.Column(db.Integer, primary_key= True)
	proveedor = db.Column(db.String(255))
	nomComer = db.Column(db.String(255))
	fol_entrada = db.Column(db.String(30))
	fecha = db.Column(db.Date)
	factura = db.Column(db.String(2))
	nFactura = db.Column(db.String(15))
	ordenCompra = db.Column(db.String(15))
	depSolici = db.Column(db.String(150))
	nReq = db.Column(db.String(15))
	oSolicitnte = db.Column(db.String(30))
	tCompraContrato = db.Column(db.String(20))
	total = db.Column(db.Float)
	observaciones = db.Column(db.Text)
	actividad = db.Column(db.Text)

	def __init__(self, proveedor, nomComer, fol_entrada, fecha, factura, nFactura, ordenCompra,
		depSolici, nReq, oSolicitnte, tCompraContrato, total, observaciones,actividad):
		self.proveedor = proveedor
		self.nomComer = nomComer
		self.fol_entrada = fol_entrada
		self.fecha = fecha
		self.factura = factura
		self.nFactura = nFactura
		self.ordenCompra = ordenCompra
		self.depSolici = depSolici
		self.nReq = nReq
		self.oSolicitnte = oSolicitnte
		self.tCompraContrato = tCompraContrato
		self.total = total
		self.observaciones = observaciones
		self.actividad = actividad


class Salida_Articulos(db.Model):
	__tablename__ = "salidaArticulos"
	id = db.Column(db.Integer, primary_key=True)
	salidas_id = db.Column(db.Integer)
	cantidad = db.Column(db.Float)
	udm = db.Column(db.String(15))
	codigo = db.Column(db.String(35))
	descripcion = db.Column(db.String(150))
	p_unit = db.Column(db.Float)
	total = db.Column(db.Float)
	ordenCompra = db.Column(db.String(15))
	imtemId = db.Column(db.Integer)

	def __init___(self, salidas_id, cantidad, udm, codigo, descripcion, p_unit, total, ordenCompra, imtemId):
		self.salidas_id = salidas_id
		self.cantidad = cantidad
		self.udm = udm
		self.codigo = codigo
		self.descripcion = descripcion
		self.p_unit = p_unit
		self.total = total
		self.ordenCompra = ordenCompra