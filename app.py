# Sistema web para la gestión del Almacén General de la CAPA
#Programadores: Cesar Herrera Mut, Hugo Canul Echazarreta ( Septiembre de 2018)
#Analista Profesional - Dirección de Informática - Direccion General
#Desarrollado en Python 3.4
#Si no logro terminarlo en diciembre va rodar mi cabeza :7 : Ya! carnal ya no Rodo tu cabeza....../ 
#      
#      (° °)
#        ~
#     --| |--
#       | |
#       | |
#
#
#
from flask import url_for
from flask import Flask, flash, redirect, render_template, request, session, abort
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from forms import Create_Form, LoginForm, formbuscap, formbuscaentrada, form_salida_orden, form_consul_entrada, formbuscasalida
import os
from models import db, User, Inventario, Articulos, Entrada, Salidas, Salida_Articulos

from config import DevelopmentConfig
import pymssql 
from bs4 import BeautifulSoup
from flask_wtf import CSRFProtect
from tools.fpdf import entradaPdf

###########################################
# CONEXION A MYSQL
# creo la importacion 
import pymysql

pymysql.install_as_MySQLdb()
###########################################


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
crsf = CSRFProtect()

#################################################
# CONEXION A SQL SERVER 2012
# Creo la cadena de conexion 
server ="DESKTOP-TRVGHH8\\SQLHUGO"
user="sa"
password="12345"
base ="capa"
connection = pymssql.connect(host=server, user=user, password=password, database=base)

try :
   # Creacion del cursor
   cursor = connection.cursor()  
   print("Conexion establecida con exito")
except:
   print("No hay Conexion a SQL SERVER")
####################################################

def listaGlobal(lista):
	listatotal=[]
	for item in lista:
		if len(item) == 9:
			del item[7]
			listatotal.append(item)
		else:
			listatotal.append(item)
	return listatotal


@app.before_request
def before_request():
	if 'username' not in session and request.endpoint in ['index', 'entradas', 'salidas', 'buscaprod', 'verlista', 'ConsultaEntrada', 'crearUser', 'EntradaOrden', 'ConsultaSalida']:
		return redirect(url_for('login'))
	elif 'username' in session:
		usr = session['username']
		if request.endpoint in ['login']:
			return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    if 'username' in session:
    	nombre = (session['username']).upper()
    	return render_template('404.html', nombre=nombre), 404
    else:
    	return render_template('404.html'), 404


@app.errorhandler(400)
def regreso(e):
    nombre = (session['username']).upper()
    x = request.endpoint
    if x=='salidas':
    	nombre = session['username']
    	form = formbuscasalida(request.form)
    	return render_template("salidas.html", form=form, nombre=nombre)
    elif x == 'buscaprod2':
    	nombre = session['username']
    	form_buscap = formbuscap(request.form)
    	return render_template("buscar.html", nombre=nombre, form=form_buscap)
    return render_template(x + '.html', nombre=nombre), 400


# Paso en la url un nombre de usuario
@app.route("/index/")
@app.route("/")
def index():
	if 'username' in session:
		nombre = session['username'].upper()
		return render_template("index.html",nombre=nombre)
	else:
		return redirect(url_for('login'))


@app.route('/crearUser', methods=['GET', 'POST'])
def crearUser():
    pri = ""
    crear = Create_Form(request.form)
    if request.method == 'POST' and crear.validate():
        user = crear.username.data
        usuar = User.query.filter_by(username=user).first()
        if usuar is None:
                user = User(crear.username.data,
                            crear.password.data,
                            crear.email.data,
                            )
                db.session.add(user)
                db.session.commit()
                succes_message = 'Usuario registrado en la base de datos'
                flash(succes_message)
                return redirect(url_for('crearUser'))
        else:
            succes_message = 'El usuario existe en la base de datos'
            flash(succes_message)
            return redirect(url_for('crearUser'))
    nombre = (session['username']).upper()
    return render_template('crearUser.html', form=crear, nombre=nombre)


@app.route('/entradas', methods=['GET', 'POST'])	
def entradas():
	nombre = session['username'].upper()
	form_buscaentrada = formbuscaentrada(request.form)
	if request.method == 'POST':
		if 'buscar' in request.form['addentrada']:
			print('Entradas-Boton buscar funcionando')
	else:
		print("Entradas-No entro al método POST")
	return render_template("entradas.html", form=form_buscaentrada, nombre=nombre)
	
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	username_ =""
	password_ =""
	login_form = LoginForm(request.form) 
	if request.method == 'POST' and login_form.validate() :
		username = login_form.username.data
		password = login_form.password.data
		user = User.query.filter_by(username=username).first()
		#Buscamos en el cursor los primeros dos campos que contienen usuario y contraseña
		if user is not None and user.verify_password(password):
			sucess_message = 'Bienvenido {}'.format(username)
			flash(sucess_message)
			session['username'] = username
			session['listatotal']=[]
			return redirect(url_for('index'))
		else:
			error_message = '{} No es un usuario del sistema'.format(username)
			flash(error_message)
			return redirect(url_for('login'))
	return render_template('login.html', form = login_form)


@app.route('/logout')
def logout():
	if 'username' in session:
		#connection.close()
		session.pop('listatotal')
		session.pop('username')		    
	return redirect(url_for('login'))


@app.route('/buscaprod', methods=['GET', 'POST'])
def buscaprod():
	nombre = session['username']
	form_buscap = formbuscap(request.form)
	if request.method == 'POST':
		ArtCodigo = form_buscap.product_id.data
		ArtName = form_buscap.product_name.data
		print(request.form['addsalida'])
		if 'mostrar' in request.form['addsalida']:
			print(session['listatotal'])
			return render_template("buscar.html", nombre=nombre, form=form_buscap, listatemp2=session['listatotal'])
		elif 'entrada' in request.form['addsalida']:
			x = request.form.getlist('cantidad')
			y = request.form.getlist('costo')
			print(x)
			print(y)
			indice =0
			
			nlista=[]
			for item in session['listatotal']:
				if x[indice]=="":
					item.append(1)
				else:
					item.append(str(float(x[indice])))
				item[6]=y[indice]
				indice+=1
				nlista.append(item)
			session.pop('listatotal')
			session['listatotal']=nlista
			print(session['listatotal'])
			return redirect(url_for('EntradaOrden'))
		elif 'eliminar' in request.form['addsalida']:
			indice=0
			elementos = request.form.getlist('optcheck')
			for i in elementos:
				for x in session['listatotal']:
					indice+=1
					if i in x:
						print(indice-1)
						temporal = session['listatotal']
						temporal.pop(indice-1)
						session.pop('listatotal')
						session['listatotal']=temporal
					else:
						pass
			return render_template("buscar.html", nombre=nombre, form=form_buscap, listatemp2=session['listatotal'])
		elif 'selec' in request.form['addsalida']:
			
			valor = request.form['optradio']
			print(valor)
			if valor:
				buscaitem = """SELECT PRODUCT.PRODUCT_ID,INTERNAL_NAME,PRODUCT_TYPE_ID,FAMILIA_ID,INVENTORY_ITEM_ID, INVENTORY_ITEM.QUANTITY_ON_HAND_TOTAL, INVENTORY_ITEM.UNIT_COST FROM PRODUCT,INVENTORY_ITEM WHERE INVENTORY_ITEM_ID = '%s' AND PRODUCT.PRODUCT_ID = INVENTORY_ITEM.PRODUCT_ID"""%valor
				cursor.execute(buscaitem)
				c_local = cursor.fetchall()
				#local = Inventario.query.filter_by(id_item=request.form['optradio']).one()
				local = c_local[0]
				li=list()
				lis=list()
				li.append(local[0])
				li.append(local[1])
				li.append(local[2])
				li.append(str(local[3]))
				li.append(str(local[4]))
				li.append(str(local[5]))
				li.append(str(local[6]))
				lis.append(li)
				session['listatotal'] += lis
				print(session['listatotal'])
				return render_template("buscar.html", nombre=nombre, form=form_buscap)
			else:
				flash("Debe elegir un articulo")
				return render_template("buscar.html", nombre=nombre, form=form_buscap)
		elif 'buscar' in request.form['addsalida']:
			#Buscar por codigo
			if ArtCodigo:
				print("buscar x codigo")

				LocalCodigo = Inventario.query.filter_by(id_prod=ArtCodigo).all()
				
				return render_template("buscar.html", nombre=nombre, form=form_buscap, listatemp=LocalCodigo)
			elif ArtName:
				print("buscar x Nombre")
				#Buscar por nombre	
				pxn='%'+ArtName+'%'
				buscapxn = """SELECT PRODUCT.PRODUCT_ID, INTERNAL_NAME, PRODUCT_TYPE_ID, FAMILIA_ID, INVENTORY_ITEM_ID, INVENTORY_ITEM.QUANTITY_ON_HAND_TOTAL, INVENTORY_ITEM.UNIT_COST  FROM PRODUCT,INVENTORY_ITEM WHERE PRODUCT_NAME LIKE '%s' AND PRODUCT.PRODUCT_ID = INVENTORY_ITEM.PRODUCT_ID"""%pxn
				cursor.execute(buscapxn)
				Localname=list()
				LocalName = cursor.fetchall()
				print(LocalName)
				#Localname = db.session.execute(buscapxn).fetchall()
				#LocalName = db.session.query(Inventario).filter(Inventario.nom_prod.like('%'+ArtName+'%')).all()
				return render_template("buscar.html", nombre=nombre, form=form_buscap, listatemp=LocalName,productpxn=ArtName)
		else:
			flash("Debe Llenar un campo")
	return render_template("buscar.html", nombre=nombre, form=form_buscap)


@app.route('/entradasAlmacen/OrdenCompra', methods=['GET', 'POST'])
def EntradaOrden():
	nombre = session['username']
	form = form_salida_orden(request.form)
	if request.method == 'POST':
		proveedor = str(form.proveedor.data).replace('(','').replace("'",'').replace(')','').replace(',','')
		fecha = form.fecha.data
		nomComer = str(form.nomComer.data).replace('(','').replace("'",'').replace(')','').replace(',','')
		folio = form.folio.data
		factura = form.factura.data
		numFactura = form.numFactura.data
		orden1 = form.orden.data
		dep_soli = str(form.dep_soli.data).replace('(','').replace("'",'').replace(')','').replace(',','')
		nReq = form.nReq.data
		oSoli = form.oSoli.data
		tCompra = form.tCompra.data
		obser = form.obser.data
		total = form.total.data
		if len(proveedor) < 5:
			flash("El campo {} es requerido".format('Proveedores'))
		elif len(str(fecha))< 5:
			flash("El campo {} es requerido".format("Fecha"))
		elif len(str(nomComer))< 5:
			flash("El campo {} es requerido".format("Nombre Comercial"))
		# elif len(str(folio))< 5:
		# 	flash("El campo {} es requerido".format("Folio"))
		elif len(str(factura))< 1:
			flash("El campo {} es requerido".format("Factura"))
		elif len(str(numFactura))< 1:
			flash("El campo {} es requerido".format("Número de Factura"))
		elif len(str(orden1))< 1:
			flash("El campo {} es requerido".format("Orden de Compra"))
		elif len(str(dep_soli))< 5:
			flash("El campo {} es requerido".format("Departamento Solicitante"))
		# elif len(str(nReq))< 1:
		# 	flash("El campo {} es requerido".format("Número de Requerimiento"))
		elif len(str(oSoli))< 5:
			flash("El campo {} es requerido".format("Oficio Solicitante"))
		# elif len(str(tCompra))< 5:
		# 	flash("El campo {} es requerido".format("Tipo de Compra"))
		elif len(str(obser)) < 5:
			flash("El campo {} es requerido".format("Observaciones"))
		else:
			query = Entrada.query.filter_by(ordenCompra=orden1)
			datos=0
			for dato in query:
				datos = dato.id
			if datos == 0:
				Entra = Entrada(proveedor,
					nomComer,
					folio,
					fecha,
					factura,
					numFactura,
					orden1,
					dep_soli,
					nReq,
					oSoli,
					tCompra,
					total,
					obser,
				)
				generales=list()
				generales.append(proveedor)
				generales.append(fecha)
				generales.append(nomComer)
				generales.append(folio)
				generales.append(factura)
				generales.append(numFactura)
				generales.append(orden1)
				generales.append(dep_soli)
				generales.append(nReq)
				generales.append(oSoli)
				generales.append(tCompra)
				generales.append(total)
				generales.append(obser)
				db.session.add(Entra)
				db.session.commit()
				query = Entrada.query.filter_by(ordenCompra=orden1)
				for dato in query:
					datos = dato.id
				for item in session['listatotal']:
					total = float(item[0])*float(item[4])
					arti = Articulos(entradas_id = datos,
						cantidad = item[0],
						udm = item[5],
						codigo = item[1],
						descripcion = item[3],
						p_unit = item[4],
						total = total,
						ordenCompra = orden1,
						imtemId = item[2],)
					db.session.add(arti)
					db.session.commit()
					canti = Inventario.query.filter_by(id_item = item[2]).one()
					print(canti)
					saldo = canti.cant_exist
					print(saldo)
					t = float(item[0])+ float(saldo)
					print(t)
					canti.cant_exist = t
					db.session.commit()
				flash("Entrada Núm {} Realizada con exito".format(datos))
				listas = list()
				listas.append('Proveedor:')
				listas.append('Nombre Comercial:')
				x = entradaPdf("Entrada", listas, generales, session['listatotal'])
				session.pop('listatotal')
				session['listatotal']=[]
				return x
			else:
				flash("La orden núm. {} ya ha sido capturada anteriormente".format(orden1))
	return render_template("entradaOrden.html", nombre=nombre, form=form, listaglobal=session['listatotal'])


@app.route('/consultayreportes/reimpresiondeE_S/entradas', methods=['GET', 'POST'])
def ConsultaEntrada():
	nombre = session['username'] 
	form = form_consul_entrada(request.form)
	if request.method == 'POST':
		orden = form.nOrden.data
		xa = request.form['addOrdenSal'][:10]
		if 'reimprimir' in xa:
			query = Entrada.query.filter_by(ordenCompra=request.form['addOrdenSal'][10:]).one()
			arti = Articulos.query.filter_by(ordenCompra = request.form['addOrdenSal'][10:]).all()
			generales=list()
			generales.append(query.proveedor)
			generales.append(query.fecha)
			generales.append(query.nomComer)
			generales.append(query.fol_entrada)
			generales.append(query.factura)
			generales.append(query.nFactura)
			generales.append(query.ordenCompra)
			generales.append(query.depSolici)
			generales.append(query.nReq)
			generales.append(query.oSolicitnte)
			generales.append(query.tCompraContrato)
			generales.append(query.total)
			generales.append(query.observaciones)
			listas = list()
			listas.append('Proveedor:')
			listas.append('Nombre Comercial:')
			x = entradaPdf("Entrada Reimpresa", listas, generales, arti,1)
			return x
		elif 'buscarOrd' in xa:
			try:
				entra = Entrada.query.filter_by(ordenCompra = orden).one()
			except Exception as e:
				entra = 0
			finally:
				arti = Articulos.query.filter_by(ordenCompra = orden).all()
			if entra == 0:
				flash("El numero de orden no existe")
			else:
				return render_template("entradaOrden.html", nombre=nombre, reporte=entra, form=form, lista=arti)
	return render_template("consulta.html", nombre=nombre, form=form, titulo="Entradas")


@app.route('/salidas_de_almacen/salidas_por_orden_de_compra', methods=['GET', 'POST'])	
def salidas():	
	nombre = session['username'].upper()
	form_buscasalida = formbuscasalida(request.form)
	if request.method == 'POST':
		print("RECIBIO NUMERO DE ORDEN DE SALIDA ")
		#print(request.form['addOSalida'])
		id_orden = form_buscasalida.order_id.data
		print(len(id_orden))
		# if len(id_orden)==0:
		# 	flash('Debe capturar un numero de orden')
		# 	return redirect(url_for('salidas'))
		if id_orden:			
			if 'buscar' in request.form['addentrada']:
				SqlQueryE = """SELECT * FROM entradas  WHERE entradas.ordencompra='%s'"""%(id_orden)
				SqlQueryD = """SELECT * FROM entarti  WHERE entarti.ordencompra='%s'"""%(id_orden)
				Enc_Orden = db.session.execute(SqlQueryE).fetchall()
				Det_Orden = db.session.execute(SqlQueryD).fetchall()
				verifica = Salidas.query.filter_by(ordenCompra=id_orden).first()
				print(verifica)
				if verifica:
					flash('El numero de orden ya ha sido capturado')
					return redirect(url_for('salidas'))
				if len(Enc_Orden)==0:
					flash('El numero de orden no existe')
					return redirect(url_for('salidas'))
				if Enc_Orden:
					EncabeOrden = Enc_Orden[0]
					print(Enc_Orden)
					DetalleOrden = Det_Orden
				return render_template("SalidaOrden.html", nombre=nombre,form=form_buscasalida,DetalleOrden=DetalleOrden,EncabeOrden=EncabeOrden)	
		elif 'guardaSalida' in request.form['addOSalida'][:12]:
			actividad = form_buscasalida.actividad.data
			verifica = Salidas.query.filter_by(ordenCompra=request.form['addOSalida'][:12]).first()
			if verifica==None:
				if len(form_buscasalida.actividad.data)==0:
					error_message = 'Debe capturar una actividad'
					flash(error_message)
					return redirect(url_for('salidas'))
				print(request.form['addOSalida'][12:])
				Enc_Orden = Entrada.query.filter_by(ordenCompra=request.form['addOSalida'][12:]).one()
				Det_Orden = Articulos.query.filter_by(ordenCompra=request.form['addOSalida'][12:]).all()
				print(Det_Orden)
				print(Enc_Orden.nomComer)
				Sali = Salidas(Enc_Orden.proveedor,
					Enc_Orden.nomComer,
					Enc_Orden.fol_entrada,
					Enc_Orden.fecha,
					Enc_Orden.factura,
					Enc_Orden.nFactura,
					Enc_Orden.ordenCompra,
					Enc_Orden.depSolici,
					Enc_Orden.nReq,
					Enc_Orden.oSolicitnte,
					Enc_Orden.tCompraContrato,
					Enc_Orden.total,
					Enc_Orden.observaciones,
					form_buscasalida.actividad.data,
				)
				db.session.add(Sali)
				db.session.commit()
				salida_id = Salidas.query.filter_by(ordenCompra=Enc_Orden.ordenCompra).first()
				print(salida_id.id)
				for item in Det_Orden:
					Sali_art = Salida_Articulos(salidas_id=salida_id.id,
						cantidad=item.cantidad,
						udm=item.udm,
						codigo=item.codigo,
						descripcion=item.descripcion,
						p_unit=item.p_unit,
						total=item.total,
						ordenCompra=item.ordenCompra,
						imtemId=item.imtemId,
						)
					db.session.add(Sali_art)
					db.session.commit()
					canti = Inventario.query.filter_by(id_item = item.imtemId).one()
					print(canti)
					saldo = canti.cant_exist
					print(saldo)
					t = float(saldo) - item.cantidad
					print(t)
					canti.cant_exist = t
					db.session.commit()
				arti = Salida_Articulos.query.filter_by(ordenCompra = Enc_Orden.ordenCompra).all()
				query = Salidas.query.filter_by(ordenCompra=Enc_Orden.ordenCompra).one()
				generales=list()
				generales.append(query.proveedor)
				generales.append(query.fecha)
				generales.append(query.nomComer)
				generales.append(query.fol_entrada)
				generales.append(query.factura)
				generales.append(query.nFactura)
				generales.append(query.ordenCompra)
				generales.append(query.depSolici)
				generales.append(query.nReq)
				generales.append(query.oSolicitnte)
				generales.append(query.tCompraContrato)
				generales.append(query.total)
				generales.append(query.actividad)
				listas = list()
				listas.append('Proveedor:')
				listas.append('Nombre Comercial:')
				x = entradaPdf("Salida", listas, generales, arti,1)
				return x
		elif len(id_orden)==0:
			print("XXXXXXXXXXXXXXXXXXXXX")
			error_message = 'Debe capturar un numero de orden'
			flash(error_message)
			return redirect(url_for('salidas'))
	return render_template("salidas.html", form=form_buscasalida, nombre=nombre)


@app.route('/consultayreportes/reimpresiondeE_S/salidas', methods=['GET', 'POST'])
def ConsultaSalida():
	nombre = session['username'] 
	form = form_consul_entrada(request.form)
	if request.method == 'POST':
		orden = form.nOrden.data
		xa = request.form['addOrdenSal'][:10]
		print(xa)
		if 'reimprimir' in xa:
			query = Salidas.query.filter_by(ordenCompra=request.form['addOrdenSal'][10:]).one()
			arti = Salida_Articulos.query.filter_by(ordenCompra = request.form['addOrdenSal'][10:]).all()
			generales=list()
			generales.append(query.proveedor)
			generales.append(query.fecha)
			generales.append(query.nomComer)
			generales.append(query.fol_entrada)
			generales.append(query.factura)
			generales.append(query.nFactura)
			generales.append(query.ordenCompra)
			generales.append(query.depSolici)
			generales.append(query.nReq)
			generales.append(query.oSolicitnte)
			generales.append(query.tCompraContrato)
			generales.append(query.total)
			generales.append(query.observaciones)
			listas = list()
			listas.append('Proveedor:')
			listas.append('Nombre Comercial:')
			x = entradaPdf("Salida Reimpresa", listas, generales, arti,1)
			return x
		elif 'buscarOrd' in xa:
			try:
				entra = Salidas.query.filter_by(ordenCompra = orden).one()
			except Exception as e:
				entra = 0
			finally:
				arti = Salida_Articulos.query.filter_by(ordenCompra = orden).all()
			if entra == 0:
				flash("El numero de orden no existe")
			else:
				return render_template("entradaOrden.html", nombre=nombre, reporte=entra, form=form, lista=arti)
	return render_template("consulta.html", nombre=nombre, form=form, titulo="Salidas")

	
if __name__ == '__main__':
    crsf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=8000, host='0.0.0.0')