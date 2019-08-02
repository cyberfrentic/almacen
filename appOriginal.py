# Sistema web para la gestión del Almacén General de la CAPA
#Programadores: Cesar Herrera Mut, Hugo Canul Echazarreta ( Septiembre de 2018)
#Analista Profesional - Dirección de Informática - Direccion General y Jefe depto Org. Op. FCP Q.Roo
#Desarrollado en Python 3.4
#No logré terminarlo en diciembre, pero las pantallas enviadas sirvieron para
#justificar en contraloría
#
#     ---------|--
#		| 	   |
#       |    (° °)
#       | 	    O...
#		|
#		|
#	    |
#
from flask import url_for
from flask import Flask, flash, redirect, render_template, request, session
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from forms import Create_Form, LoginForm, formbuscap, formbuscaentrada, form_salida_orden, form_consul_entrada, formbuscasalida, formActInven
import os
from models import db, User, Inventario, Articulos, Entrada, Salidas, Salida_Articulos, Historia
from datetime import datetime
import time
from config import DevelopmentConfig
import pymssql
from bs4 import BeautifulSoup
from flask_wtf import CSRFProtect
from tools.fpdf import entradaPdf
from tools.fpdf2 import entradasQuery, InventarioQuery
from sqlalchemy import or_, extract

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
# server ="DESKTOP-TRVGHH8\\SQLHUGO"
# user="sa"
# password="12345"
# base ="capa"
# connection = pymssql.connect(host=server, user=user, password=password, database=base)

# try :
#    #Creacion del cursor
#    cursor = connection.cursor()
# except:
#    print("No hay Conexion a SQL SERVER")
####################################################


@app.before_request
def before_request():
	if 'username' not in session and request.endpoint in ['index', 'entradas', 'salidas', 'buscaprod', 'verlista',
	 'ConsultaEntrada', 'crearUser', 'EntradaOrden', 'ConsultaSalida', 'salidasTit', 'SalidaPar', 'salidasImp', 'correcionSD',
	 'cancelaMix','saldosInvFis']:
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
    if x =='salidas':
    	nombre = session['username']
    	form = formbuscasalida(request.form)
    	return render_template("salidas.html", form=form, nombre=nombre), 400
    elif x == 'buscaprod2':
    	nombre = session['username']
    	form_buscap = formbuscap(request.form)
    	return render_template("buscar.html", nombre=nombre, form=form_buscap), 400
    # elif x == 'modiProd':
    # 	nombre = session['username']
    # 	form =  formActInven(request.form)
    # 	return render_template("modiProd.html", form=form, nombre=nombre), 400
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
                        crear.nombrecompleto.data,
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


@app.route('/salidasTit', methods=['GET', 'POST'])
def salidasTit():
	nombre = session['username'].upper()
	form_buscaentrada = formbuscaentrada(request.form)
	if request.method == 'POST':
		if 'buscar' in request.form['addentrada']:
			print('Salidas-Boton buscar funcionando')
	else:
		print("Entradas-No entro al método POST")
	return render_template("salidasTit.html", form=form_buscaentrada, nombre=nombre)


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
			session['listasalida']=[]
			session['total']=0
			session['total2']=0
			session['nombrecompleto']=user.nombrecompleto
			return redirect(url_for('index'))
		else:
			error_message = '{} No es un usuario del sistema'.format(username)
			flash(error_message)
			return redirect(url_for('login'))
	return render_template('login.html', form = login_form)


@app.route('/logout')
def logout():
	session.clear()
	if 'username' in session:
		#connection.close()
		session.pop('listatotal')
		session.pop('username')
		session.pop('listasalida')
		session.pop('total')
		session.pop('total2')
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
			cantidades = request.form.getlist('cantidad')
			print(cantidades)
			total_lista = 0
			pos_cant = 0
			for tupla in session['listatotal']:
				total_lista += float(tupla[7])*float(tupla[8])
				pos_cant += 1
			return render_template("buscar.html", nombre=nombre, form=form_buscap, listatemp2=session['listatotal'],total_lista=total_lista)
		elif 'entrada' in request.form['addsalida']:
			x = request.form.getlist('cantidad')
			y = request.form.getlist('costo')
			print(x)
			print(y)
			indice =0
			nlista=[]
			for item in session['listatotal']:
				if len(item)>8:
					tem=[item[0],item[1],item[2],item[3],item[4],item[5],item[6], item[8]]
					item=[]
					item=tem
				if x[indice]=="":
					item.append(1)
				else:
					item.append(str(float(x[indice])))
				item[7]=y[indice]
				indice+=1
				nlista.append(item)
			session.pop('listatotal')
			session['listatotal']=nlista
			return redirect(url_for('EntradaOrden'))
		elif 'eliminar' in request.form['addsalida']:
			indice=0
			elementos = request.form.getlist('optcheck')
			for i in elementos:
				for x in session['listatotal']:
					indice+=1
					if i in x:
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
				buscaitem = """SELECT PRODUCT.PRODUCT_ID,INTERNAL_NAME,PRODUCT_TYPE_ID,FAMILIA_ID,INVENTORY_ITEM_ID, INVENTORY_ITEM.QUANTITY_ON_HAND_TOTAL, PRODUCT.QUANTITY_UOM_ID, INVENTORY_ITEM.UNIT_COST FROM PRODUCT,INVENTORY_ITEM WHERE INVENTORY_ITEM_ID = '%s' AND PRODUCT.PRODUCT_ID = INVENTORY_ITEM.PRODUCT_ID"""%valor
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
				li.append(str(local[7]))
				li.append("1")
				lis.append(li)
				# Le agrego 1 a la cantidad cuando el user selecciona un producto.

				session['listatotal'] += lis

				print(session['listatotal'])

				return render_template("buscar.html", nombre=nombre, form=form_buscap,listatemp2=session['listatotal'])
			else:
				flash("Debe elegir un articulo")
				return render_template("buscar.html", nombre=nombre, form=form_buscap,listatemp2=session['listatotal'])
		elif 'buscar' in request.form['addsalida']:
			#Buscar por codigo
			if ArtCodigo:
				print("buscar x codigo")
				pxn = ArtCodigo
				buscapxn = """SELECT PRODUCT.PRODUCT_ID, INTERNAL_NAME, PRODUCT_TYPE_ID, FAMILIA_ID, INVENTORY_ITEM_ID, INVENTORY_ITEM.QUANTITY_ON_HAND_TOTAL, INVENTORY_ITEM.UNIT_COST  FROM PRODUCT,INVENTORY_ITEM WHERE PRODUCT.PRODUCT_ID LIKE '%s' AND PRODUCT.PRODUCT_ID = INVENTORY_ITEM.PRODUCT_ID"""%pxn
				cursor.execute(buscapxn)
				LocalCodigo=cursor.fetchall()
				return render_template("buscar.html", nombre=nombre, form=form_buscap, listatemp=LocalCodigo,listatemp2=session['listatotal'], productpxn=ArtCodigo)
			elif ArtName:
				print("buscar x Nombre")
				#Buscar por nombre
				pxn='%'+ArtName+'%'
				buscapxn = """SELECT PRODUCT.PRODUCT_ID, INTERNAL_NAME, PRODUCT_TYPE_ID, FAMILIA_ID, INVENTORY_ITEM_ID, INVENTORY_ITEM.QUANTITY_ON_HAND_TOTAL, INVENTORY_ITEM.UNIT_COST  FROM PRODUCT,INVENTORY_ITEM WHERE PRODUCT_NAME LIKE '%s' AND PRODUCT.PRODUCT_ID = INVENTORY_ITEM.PRODUCT_ID"""%pxn
				cursor.execute(buscapxn)
				Localname=list()
				LocalName = cursor.fetchall()
				#print(LocalName)
				#Localname = db.session.execute(buscapxn).fetchall()
				#LocalName = db.session.query(Inventario).filter(Inventario.nom_prod.like('%'+ArtName+'%')).all()
				return render_template("buscar.html", nombre=nombre, form=form_buscap, listatemp=LocalName,listatemp2=session['listatotal'], productpxn=ArtName)

		elif 'costeo' in request.form['addsalida']:
	 		if session['listatotal']:
	 			# item 6 de listatotal es el costo
	 			total_lista = 0
	 			cantidades = request.form.getlist('cantidad')
	 			print("Cantidades cantidades cantidades, recibido lista total")
	 			print(session['listatotal'])
	 			print(cantidades)
	 			# En listatotal posicion 7 estan los costos que por defecto son los del sicopa
	 			# si el usuario modifica esa cantidad esta parte de codigo las actualiza dentro de listatotal
	 			pos = 0
	 			new_cost= request.form.getlist('costo')
	 			for item in new_cost:
	 				tmp_cost= session['listatotal']
	 				j=tmp_cost[pos]
	 				# para cada lista dentro de la listatotal en la pos 8 cambia la el costo x el que el user modificó
	 				j[7] = item
	 				pos += 1
	 				session['listatotal'] = tmp_cost

	 			pos_cant = 0
	 			# Calculamos el costo total de los prods, mult costo x cant en cada tupla
	 			for tupla in session['listatotal']:
	 				total_lista += float(tupla[7])*float(cantidades[pos_cant])
	 				pos_cant += 1
	 			session['total']=total_lista
	 			pos = 0
	 			# En listatotal posicion 8 estan las cantidades que por defecto es 1
	 			# si el usuario modifica esa cantidad esta parte de codigo actualiza las cantidades dentro de listatotal
	 			for item in cantidades:
	 				tmp= session['listatotal']
	 				j=tmp[pos]
	 				# para cada lista dentro de la listatotal en la pos 7 cambia la cant que el user indicó
	 				j[8] = item
	 				pos += 1
	 				session['listatotal'] = tmp
	 			print("Lista final para Entrada")
	 			print(session['listatotal'])
	 			print("total_lista")
	 			print(total_lista)
	 			return render_template("buscar.html", nombre=nombre, form=form_buscap, listatemp2=session['listatotal'],total_lista=total_lista)
		else:
			flash("Debe Llenar un campo")
	return render_template("buscar.html", nombre=nombre, form=form_buscap,listatemp2=session['listatotal'])


@app.route('/entradasAlmacen/OrdenCompra', methods=['GET', 'POST'])
def EntradaOrden():
	nombre = session['username']
	form = form_salida_orden(request.form)
	if request.method == 'POST':
		proveedor = str(form.proveedor.data).replace('(','').replace("'",'').replace(')','').replace(',','')
		fecha = form.fecha.data
		nomComer = str(form.nomComer.data).replace('(','').replace("'",'').replace(')','').replace(',','')
		folio = folio_e()
		factura = form.factura.data
		numFactura = form.numFactura.data
		orden1 = form.orden.data
		dep_soli = str(form.dep_soli.data).replace('(','').replace("'",'').replace(')','').replace(',','')
		nReq = form.nReq.data
		oSoli = form.oSoli.data
		tCompra = form.tCompra.data
		obser = form.obser.data
		total = session['total']

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
                    session['nombrecompleto'],
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
				generales.append(session['nombrecompleto'])
				db.session.add(Entra)
				db.session.commit()
				query = Entrada.query.filter_by(ordenCompra=orden1)
				for dato in query:
					datos = dato.id

				print("Listatotal para entradas antes de darle boton guardar")
				print(session['listatotal'])
				for item in session['listatotal']:
					#print(item)
					total = float(item[8])*float(item[7])
					arti = Articulos(entradas_id = datos,
						cantidad = item[8],
						udm = item[6],
						codigo = item[0],
						descripcion = item[1],
						p_unit = item[7],
						total = total,
						ordenCompra = orden1,
						imtemId = item[4],)
					db.session.add(arti)
					db.session.commit()
					inve = Inventario(
						id_item = item[4],
						id_prod = item[0],
						tipo_prod = item[2],
						nom_prod = item[1],
						nom_interno = item[1],
						descripcion = item[1],
						um = item[6],
						id_area = None,
						activo = None,
						id_familia = None,
						procedencia = None,
						modelo = None,
						num_parte = None,
						num_serie = None,
						cant_exist = item[8],
						cant_dispon = item[8],
						costo_unit = item[7],
						moneda= "MX",
						id_area_solici = None,
						solic_transfer = None,
						observaciones = obser,
						usuario = session['username'],
						fol_entrada = orden1,
						fol_salida = None,
						oficio_e_s = oSoli,
						id_proveed = proveedor[:19],
						orden_compra = orden1,
						num_requerim = nReq,
						n_fact_nota = numFactura,
						f_salida = fecha,
						tipo_compra = None,
						actividad='Entrada',
						id=None
						)
					db.session.add(inve)
					db.session.commit()
				flash("Entrada Núm {} Realizada con exito".format(datos))
				listas = list()
				listas.append('Proveedor:')
				listas.append('Nombre Comercial:')
				print(listas)
				#print(generales)
				x = entradaPdf("Entrada", listas, generales, session['listatotal'])
				session.pop('listatotal')
				session.pop('total')
				session['listatotal']=[]
				session['total']=0
				return x
			else:
				flash("La orden núm. {} ya ha sido capturada anteriormente".format(orden1))
	return render_template("entradaOrden.html", nombre=nombre, form=form, listaglobal=session['listatotal'], folio_e=folio_e(), total1=session['total'])


@app.route('/consultayreportes/reimpresiondeE_S/entradas', methods=['GET', 'POST'])
def ConsultaEntrada():
	nombre = session['username']
	form = form_consul_entrada(request.form)
	if request.method == 'POST':
		busqueda =  request.form.get('optradio')
		orden = form.nOrden.data
		xa = request.form['addOrdenSal']
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
			generales.append(query.nombrerecibe)
			listas = list()
			listas.append('Proveedor:')
			listas.append('Nombre Comercial:')
			x = entradaPdf("Entrada", listas, generales, arti,1)
			return x
		elif 'buscarOrd' in xa:
			if busqueda == '8':
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
			elif busqueda == '1':
				try:
					entra = Entrada.query.filter_by(proveedor = orden).all()
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Proveedor", buscado=orden)
			elif busqueda == '2':
				try:
					entra = Entrada.query.filter_by(nFactura = orden).all()
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Factura", buscado=orden)
			elif busqueda == '3':
				if "/" in orden:
					d,m,a = orden.split('/')
				elif "-" in orden:
					flash("utilice el formato dd/mm/aaaa")
					return redirect(url_for("ConsultaEntrada"))
				if len(a)==2:
					an ="20" + a
				elif len(a)==4:
					an = a
				orden = an +"-"+m+"-"+d
				print(orden)
				try:
					entra = Entrada.query.filter_by(fecha = orden).all()
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Factura", buscado=orden)
			elif busqueda == '4':
				ord = "%"+orden+"%"
				print(ord)
				try:
					print("sinentra")
					entra = Articulos.query.filter(Articulos.descripcion.like(ord)).group_by(Articulos.ordenCompra).all()
					print(entra)
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Articulos", buscado=orden)
			elif busqueda == '5':
				try:
					entra = Entrada.query.filter_by(tCompraContrato = orden).all()
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Tipo Compra Contrato", buscado=orden)
			elif busqueda == '6':
				print(orden)
				try:
					entra = Entrada.query.filter(Entrada.nombrerecibe.like("%"+orden+"%")).all()
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Nombre Solicitante", buscado=orden)
			elif busqueda == '7':
				print(orden)
				try:
					entra = Entrada.query.filter_by(oSolicitnte = orden).all()
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Tipo Compra Contrato", buscado=orden)
		if "proveedor" in xa:
			a, b = xa.split(".")
			entra = Entrada.query.filter_by(ordenCompra = b).one()
			try:
				entra = Entrada.query.filter_by(ordenCompra = b).one()
			except Exception as e:
				print(e)
				entra = 0
			finally:
				arti = Articulos.query.filter_by(ordenCompra = b).all()
			if entra == 0:
				flash("El numero de orden no existe")
			else:
				return render_template("entradaOrden.html", nombre=nombre, reporte=entra, form=form, lista=arti, titulo="Entradas")
	return render_template("consulta.html", nombre=nombre, form=form, titulo="Entradas")

##falta modificar
@app.route('/salidas_de_almacen/salidas_por_orden_de_compra', methods=['GET', 'POST'])
def salidas():
	nombre = session['username'].upper()
	form_buscasalida = formbuscasalida(request.form)
	if request.method == 'POST':
		print("RECIBIO NUMERO DE ORDEN DE SALIDA ")
		id_orden = form_buscasalida.order_id.data
		if id_orden:
			print(id_orden)
			if 'buscar' in request.form['addentrada']:
				SqlQueryE = """SELECT * FROM entradas  WHERE entradas.ordencompra='%s'"""%(id_orden)
				SqlQueryD = """SELECT * FROM entarti  WHERE entarti.ordencompra='%s'"""%(id_orden)
				Enc_Orden = db.session.execute(SqlQueryE).fetchall()
				Det_Orden = db.session.execute(SqlQueryD).fetchall()
				verifica = Salidas.query.filter_by(ordenCompra=id_orden).first()
				#print(verifica)
				if verifica:
					flash('El numero de orden ya ha sido capturado')
					return redirect(url_for('salidas'))
				if len(Enc_Orden)==0:
					flash('El numero de orden no existe')
					return redirect(url_for('salidas'))
				if Enc_Orden:
					# EncabeOrden = Enc_Orden[0]
					# DetalleOrden = Det_Orden
					DetalleOrden = Det_Orden
					#Convierto EncOrden en listas poder modificarlo
					Enc_Orden = [list(fila) for fila in Enc_Orden]
					EncabeOrden = Enc_Orden[0]
					#Convierto la lista de tuplas DetalleOrden en listas poder modificarlos
					DetalleOrden = [list(fila) for fila in DetalleOrden]
					print("ENCABEZADO Y DETALLE DE LA ORDEN")
					print(EncabeOrden)
					print(DetalleOrden)
					total_orden = 0
					for lista in DetalleOrden:
						#Calculamos el total del renglon cant x costo
						lista[7] = lista[2] * lista[6]
						#Sumo total de renglones para obtener total general
						total_orden = total_orden + lista[7]
					#Actualizo el costo del encabezado
					EncabeOrden[12]	= total_orden
					session['totalNSalida'] = str(total_orden)
				return render_template("SalidaOrden.html", nombre=nombre,form=form_buscasalida,DetalleOrden=DetalleOrden,EncabeOrden=EncabeOrden)
		elif 'guardaSalida' in request.form['addOSalida'][:12]:
			actividad = form_buscasalida.actividad.data
			nombrerecibe = request.form.get('recibe')
			verifica = Salidas.query.filter_by(ordenCompra=request.form['addOSalida'][:12]).first()
			if verifica==None:
				if len(form_buscasalida.actividad.data)==0:
					error_message = 'Debe capturar una actividad'
					flash(error_message)
					return redirect(url_for('salidas'))
				#print(request.form['addOSalida'][12:])
				Enc_Orden = Entrada.query.filter_by(ordenCompra=request.form['addOSalida'][12:]).one()
				Det_Orden = Articulos.query.filter_by(ordenCompra=request.form['addOSalida'][12:]).all()
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
					session['totalNSalida'],
					Enc_Orden.observaciones,
					form_buscasalida.actividad.data,
					nombrerecibe,
					session['username'],
				)
				db.session.add(Sali)
				db.session.commit()
				salida_id = Salidas.query.filter_by(ordenCompra=Enc_Orden.ordenCompra).first()
				#print(salida_id.id)
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
					print(item.ordenCompra, item.imtemId)
					canti = Inventario.query.filter_by(orden_compra = item.ordenCompra).filter_by(id_item = item.imtemId).one()
					print(canti)
					saldo = canti.cant_exist
					print(saldo)
					t = float(saldo) - item.cantidad
					print(t)
					canti.cant_exist = t
					canti.actividad="Surtido"
					db.session.commit()
					artiSalidas = Salida_Articulos.query.filter_by(imtemId=item.imtemId).filter_by(ordenCompra=item.ordenCompra).one()
					print(artiSalidas,"----",Det_Orden[0])
					his = Historia(
						salida = salida_id.id,
						salida_articulos = artiSalidas.id, 
						entrada_articulos = Det_Orden[0].id, 
						inv = canti.id,)
					db.session.add(his)
					db.session.commit()
				arti = Salida_Articulos.query.filter_by(ordenCompra = Enc_Orden.ordenCompra).all()
				query = Salidas.query.filter_by(ordenCompra=Enc_Orden.ordenCompra).first()

				generales=list()
				generales.append(query.proveedor)
				generales.append(query.fecha)
				generales.append(nombrerecibe)#Nombre de quien recibe
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
				generales.append(query.solicitante)
				listas = list()
				listas.append('Proveedor:')
				listas.append('Nombre Comercial:')
				x = entradaPdf("Salida", listas, generales, arti,1)
				return x
		else:
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
		busqueda =  request.form.get('optradio')
		orden = form.nOrden.data
		print(busqueda)
		print(orden)
		xa = request.form['addOrdenSal']
		print(xa)
		if 'reimprimir' in xa:
			if len(request.form['addOrdenSal'][10:])==17:
				query = Salidas.query.filter_by(fol_entrada=request.form['addOrdenSal'][10:]).one()
			else:
				query = Salidas.query.filter_by(ordenCompra=request.form['addOrdenSal'][10:]).one()
			print(query)
			arti = Salida_Articulos.query.filter_by(salidas_id=query.id).all()
			generales=list()
			generales.append(query.proveedor)
			generales.append(query.fecha)
			generales.append(query.solicitante)
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
			x = entradaPdf("Salida Reimpresa", listas, generales, arti,1, query.solicitante)
			return x
		elif 'buscarOrd' in xa:
			if busqueda == '8':
				print(orden)
				try:
					entra = Salidas.query.filter_by(ordenCompra = orden).all()
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					print(entra)
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Proveedor", buscado=orden)
			elif busqueda == '1':
				print("hugo")
				try:
					entra = Salidas.query.filter_by(proveedor = orden).all()
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Proveedor", buscado=orden)
			elif busqueda == '2':
				try:
					entra = Salidas.query.filter_by(nFactura = orden).all()
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Factura", buscado=orden)
			elif busqueda == '3':
				if "/" in orden:
					d,m,a = orden.split('/')
				elif "-" in orden:
					flash("utilice el formato dd/mm/aaaa")
					return redirect(url_for("ConsultaEntrada"))
				if len(a)==2:
					an ="20" + a
				elif len(a)==4:
					an = a
				orden = an +"-"+m+"-"+d
				print(orden)
				try:
					entra = Salidas.query.filter_by(fecha = orden).all()
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Factura", buscado=orden)
			elif busqueda == '4':
				ord = "%"+orden+"%"
				print(ord)
				try:
					entra = Salida_Articulos.query.filter(Salida_Articulos.descripcion.like(ord)).group_by(Salida_Articulos.ordenCompra).all()
					print(entra)
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Articulos", buscado=orden)
			elif busqueda == '5':
				try:
					entra = Salidas.query.filter_by(tCompraContrato = orden).all()
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Tipo Compra Contrato", buscado=orden)
			elif busqueda == '6':
				print(orden)
				try:
					entra = Salidas.query.filter(Entrada.nombrerecibe.like("%"+orden+"%")).all()
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Nombre Solicitante", buscado=orden)
			elif busqueda == '7':
				print(orden)
				try:
					entra = Salidas.query.filter_by(oSolicitnte = orden).all()
				except Exception as e:
					entra = 0
				if entra == 0:
					flash("El numero de orden no existe")
				else:
					return render_template("entradaOrden2.html", nombre=nombre, lista=entra, titulo="Tipo Compra Contrato", buscado=orden)
		if "proveedor" in xa:
			a, b = xa.split(".")
			try:
				if "SalidaParcial" in b:
					entra = Salidas.query.filter_by(id = b[13:]).one()
				else:
					entra = Salidas.query.filter_by(ordenCompra = b).one()
			except Exception as e:
				print(e)
				entra = 0
			finally:
				arti = Salida_Articulos.query.filter_by(ordenCompra = b).all()
			if entra == 0:
				flash("El numero de orden no existe")
			else:
				return render_template("entradaOrden.html", nombre=nombre, reporte=entra, form=form, lista=arti,titulo="Salidas")
	return render_template("consulta.html", nombre=nombre, form=form, titulo="Salidas")


@app.route('/salidas_de_almacen/salidas_parciales', methods=['GET', 'POST'])
def SalidaPar():
	nombre = session['username']
	form = formbuscap(request.form)
	if request.method == 'POST':
		ArtCodigo =form.product_id.data
		ArtName = form.product_name.data
		print(request.form['addsalida'])
		if 'mostrar' in request.form['addsalida']:
			#print(session['listasalida'])
			# Calculamos el costo total de los prods, mult costo x cant en cada tupla
			cantidades = request.form.getlist('cantidad')
			print(cantidades)
			total_lista = 0
			pos_cant = 0
			for tupla in session['listasalida']:
				total_lista += float(tupla[7])*float(tupla[8])
				pos_cant += 1
			return render_template("buscar2.html", nombre=nombre, form=form, listatemp2=session['listasalida'],total_lista=total_lista)
		elif 'salida' in request.form['addsalida']:
			x = request.form.getlist('cantidad')
			print(x)
			print(session['listasalida'])
			indice =0
			nlista=[]
			return redirect(url_for('salidasImp'))
		elif 'eliminar' in request.form['addsalida']:
			indice=0
			elementos = request.form.getlist('optcheck')
			print(elementos)
			for i in elementos:
				for x in session['listasalida']:
					indice+=1
					if i in x:
						temporal = session['listasalida']
						temporal.pop(indice-1)
						session.pop('listasalida')
						session['listasalida']=temporal
					else:
						pass
			return render_template("buscar2.html", nombre=nombre, form=form, listatemp2=session['listasalida'])
		elif 'selec' in request.form['addsalida']:
			valor = request.form['optradio']
			print(valor)
			codigo,item,origen=valor.split(',')
			if valor:
				if origen =="inv":
					print(codigo)
					local = Inventario.query.filter(Inventario.id_item==codigo).filter(Inventario.costo_unit==item).one()
					print(local)
					li=list()
					lis=list()
					li.append(local.id_item)
					li.append(local.nom_prod)
					li.append("Stock")
					li.append(str(local.id))
					li.append(str(local.um))
					li.append(str(local.cant_exist))
					li.append(str(local.costo_unit))
					li.append("1")
					
					lis.append(li)
					print(lis)
					# Le agrego 1 a la cantidad cuando el user selecciona un producto.
					session['listasalida'] += lis
					print(session['listasalida'])
				else:
					local = Inventario.query.filter(Inventario.id_prod==codigo).filter(Inventario.orden_compra==item).one()
					print(local)
					li=list()
					lis=list()
					li.append(local.id_item)
					li.append(local.nom_prod)
					li.append(item)
					li.append(str(local.orden_compra))
					li.append(str(local.um))
					li.append(str(local.cant_exist))
					li.append(str(local.costo_unit))
					li.append("1")
					lis.append(li)
					# Le agrego 1 a la cantidad cuando el user selecciona un producto.
					session['listasalida'] += lis
					print(session['listasalida'])
				return render_template("buscar2.html", nombre=nombre, form=form,listatemp2=session['listasalida'])
			else:
				flash("Debe elegir un articulo")
				return render_template("buscar2.html", nombre=nombre, form=form,listatemp2=session['listasalida'])
		elif 'buscar' in request.form['addsalida']:
			#Buscar por codigo
			if ArtCodigo:
				print("buscar x codigo")
				pxn = ArtCodigo
				buscapxn = db.session.query(Inventario).filter(Inventario.id_prod.like('%'+ArtCodigo+'%')).filter(Inventario.actividad!="a").filter(Inventario.cant_exist>0).all()
				buscainv = db.session.query(Inventario).filter(Inventario.id_item.like('%'+ArtCodigo+'%')).filter(Inventario.actividad=="a").filter(Inventario.cant_exist>0).all()
				print(buscainv)
				return render_template("buscar2.html", nombre=nombre, form=form, listainv=buscainv,listatemp=buscapxn,listatemp2=session['listasalida'], productpxn=ArtCodigo)
			elif ArtName:
				print("buscar x Nombre")
				#Buscar por nombre
				pxn='%'+ArtName+'%'
				buscapxn = db.session.query(Inventario).filter(Inventario.nom_prod.like('%'+ArtName+'%')).filter(Inventario.actividad!="a").filter(Inventario.cant_exist>0).all()
				buscainv = db.session.query(Inventario).filter(Inventario.nom_prod.like('%'+ArtName+'%')).filter(Inventario.actividad=="a").filter(Inventario.cant_exist>0).all()
				return render_template("buscar2.html", nombre=nombre, form=form, listainv=buscainv,listatemp=buscapxn,listatemp2=session['listasalida'], productpxn=ArtName)
		elif 'costeo' in request.form['addsalida']:
	 		if session['listasalida']:
	 			# item 7 de listasalida es el costo
	 			total_lista = 0
	 			cantidades = request.form.getlist('cantidad')
	 			print("Cantidades cantidades cantidades, recibido lista total")
	 			print(session['listasalida'])
	 			print(cantidades)
	 			# En listasalida posicion 7 estan los costos que por defecto son los del sicopa
	 			# si el usuario modifica esa cantidad esta parte de codigo las actualiza dentro de listasalida
	 			pos = 0
	 			new_cost= request.form.getlist('costo')
	 			for item in new_cost:
	 				tmp_cost= session['listasalida']
	 				j=tmp_cost[pos]
	 				# para cada lista dentro de la listasalida en la pos 8 cambia la el costo x el que el user modificó
	 				j[7] = item
	 				pos += 1
	 				session['listasalida'] = tmp_cost

	 			pos_cant = 0
	 			# Calculamos el costo total de los prods, mult costo x cant en cada tupla
	 			for tupla in session['listasalida']:
	 				total_lista += float(tupla[7])*float(cantidades[pos_cant])
	 				pos_cant += 1
	 			session['total2']=total_lista
	 			pos = 0
	 			# En listasalida posicion 7 estan las cantidades que por defecto es 1
	 			# si el usuario modifica esa cantidad esta parte de codigo actualiza las cantidades dentro de listasalida
	 			for item in cantidades:
	 				tmp= session['listasalida']
	 				j=tmp[pos]
	 				# para cada lista dentro de la listasalida en la pos 7 cambia la cant que el user indicó
	 				j[5] = item
	 				pos += 1
	 				session['listasalida'] = tmp
	 			print("Lista final para Entrada")
	 			print(session['listasalida'])
	 			print("total_lista")
	 			print(total_lista)
	 			return render_template("buscar2.html", nombre=nombre, form=form, listatemp2=session['listasalida'],total_lista=total_lista)
		else:
			flash("Debe Llenar un campo")
	return render_template("buscar2.html", nombre=nombre, form=form,listatemp2=session['listasalida'])


@app.route('/salidas_de_almacen/salida-parcial/impresion', methods=['GET', 'POST'])
def salidasImp():
	nombre=session['username']
	detalle = session['listasalida']
	total = session['total2']
	form = formbuscasalida(request.form)
	form2 = form_salida_orden(request.form)
	if request.method == 'POST':
		folio = request.form['folio']
		print(folio)
		req = form2.nReq.data
		dep = form2.dep_soli.data
		oficio = form2.oSoli.data
		actividad = form.actividad.data
		nombrerecibe = request.form.get('recibe')
		if actividad and dep and oficio:
			f = time.strftime("%Y-%m-%d")
			verifica = Salidas.query.filter(Salidas.nReq==req).first()
			if verifica == None:
				sali = Salidas(proveedor = '',
						nomComer = '',
						fol_entrada = folio,
						fecha = str(f),
						factura = '',
						nFactura = '',
						ordenCompra = '',
						depSolici = str(dep),
						nReq = str(req),
						oSolicitnte = str(oficio),
						tCompraContrato = '',
						total = session['total2'],
						observaciones = '',
						actividad = str(actividad),
						solicitante=nombrerecibe,
						nombreElabora = nombre,
					)
				db.session.add(sali)
				db.session.commit()
				identificador = Salidas.query.filter(Salidas.nReq==req).filter(Salidas.fol_entrada==folio).first()
				for item in session['listasalida']:
					if item[2]=="Stock":
						cod=item[0]
						id_item = "0000"
						##### Actualiza el inventario ###### Update en SQLAlchemy
						canti = Inventario.query.filter(Inventario.id_item == cod).filter(Inventario.id==item[3]).one()
						saldo = canti.cant_exist
						t = float(saldo) - float(item[5])
						canti.cant_exist = t
						if canti.cant_exist==0:
							canti.actividad="Surtido"
						elif canti.cant_exist>0 and (len(canti.id_item)>10) :
							canti.actividad="a"
						elif ((canti.cant_exist>0) and (len(canti.id_item)<8)) :	
							canti.actividad="Psurtido"
						db.session.commit()
						###########################################################
					else:
						seek = Inventario.query.filter(Inventario.id_item == item[0]).filter(Inventario.orden_compra==item[3]).one()
						seek_articulos = Articulos.query.filter (Articulos.imtemId==item[0]).filter(Articulos.ordenCompra==item[3]).one()
						cod=seek.id_prod
						id_item = seek.id_item
						##### Actualiza el inventario ###### Update en SQLAlchemy
						#canti = Inventario.query.filter(Inventario.id_item == item[0]).filter(Inventario.orden_compra==item[3]).one()
						saldo = seek.cant_exist
						saldo_articulos = seek_articulos.cantidad
						print(saldo)
						t = float(saldo) - float(item[5])
						t2 = float(saldo_articulos) - float(item[5])
						seek.cant_exist = t
						seek_articulos.cantidad = t2
						seek_articulos.total = seek_articulos.p_unit * t2
						if seek.cant_exist==0:
							seek.actividad="Surtido"
						elif seek.cant_exist>0 :
							seek.actividad="PSurtido"
						if seek_articulos.cantidad==0:
							seek_articulos.actividad="Surtido"
						elif seek_articulos.cantidad>0 :
							seek_articulos.actividad="PSurtido"
						db.session.commit()
						###########################################################
					sa = Salida_Articulos(salidas_id = identificador.id,
							cantidad = item[5],
							udm = item[4],
							codigo = cod,
							descripcion = item[1],
							p_unit = item[6],
							total = (float(item[5])*float(item[6])),
							ordenCompra = "SalidaParcial"+str(identificador.id),
							imtemId = id_item,
						)
					db.session.add(sa)
					db.session.commit()
					########### Agregar Valores a la Tabla Hist_salidas ##############
					artiSalidas = Salida_Articulos.query.filter_by(salidas_id=identificador.id).filter_by(codigo=cod).filter_by(imtemId=id_item).first()
					if item[2]=="Stock":
						dataEntra2="Stock"
						inv = Inventario.query.filter(Inventario.id_item == cod).filter(Inventario.id==item[3]).one()
						numInv = inv.id
					else:
						dataEntra = Articulos.query.filter_by(ordenCompra=item[3]).filter_by(codigo=cod).filter_by(imtemId=id_item).one()
						dataEntra2 = dataEntra.id
						inv = Inventario.query.filter(Inventario.id_item == item[0]).filter(Inventario.orden_compra==item[3]).one()
						numInv = inv.id
					print(numInv)
					his = Historia(
						salida = artiSalidas.salidas_id,
						salida_articulos = artiSalidas.id, 
						entrada_articulos = dataEntra2, 
						inv = numInv,)
					db.session.add(his)
					db.session.commit()
					###########################################################
				flash("Salida parcial fue guardada con el numero {}".format(identificador.id))
				arti = Salida_Articulos.query.filter(Salida_Articulos.salidas_id==identificador.id).all()
				query = Salidas.query.filter(Salidas.id==identificador.id).first()
				generales=list()
				generales.append(query.proveedor)
				generales.append(query.fecha)
				generales.append(nombrerecibe) # Nombre solicitante
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
				x = entradaPdf("SalidaP", listas, generales, arti, 1, nombrerecibe)
				session.pop('listasalida')
				session.pop('total2')
				session['listasalida']=[]
				session['total2']=0
				return x
			else:
				flash("El requerimiento {} ya ha sido capturado anteriormente con numero de oficcio {}".format(req, verifica.oSolicitnte))
		else:
			flash("Debe llenar todos los campos, alguno le falto , revise por favor!")
	return render_template("SalidaParcial.html", nombre=nombre, DetalleOrden=detalle, total=total, form=form, form2=form2, folio_e=folio_e())


#FUNCION QUE GENERA EL FOLIO DE LA ENTRADA, EL FOLIO NUNCA SE REPETIRA EN EL ESPACIO-TIEMPO
def folio_e():
	a= datetime.today().year
	b=datetime.today().month
	c=datetime.today().day
	e=datetime.today()
	x = str(e)

	if len(str(b))==1:
		bb='0'+ (str(b))
	else:
		bb=str(b)

	if len(str(c))==1:
		cc='0'+ (str(c))
	else:
		cc=str(c)

	return str(a)+bb+cc+'H'+x[11:19]


@app.route('/correcciones/salidas/directas', methods=['GET','POST'])
def correcionSD():
	nombre = session['username']
	if request.method == 'POST':
		orden=request.form['orden']
		print(request.form["Cancelar"])
		if request.form["Cancelar"] == "buscar":
			try:
				data = Salidas.query.filter_by(ordenCompra = orden).one()
			except Exception as e:
				print(e)
				data=0
			if data != 0:
				dataArti = Salida_Articulos.query.filter_by(salidas_id=data.id).all()
				return render_template("correcionSD.html", nombre=nombre, data=data, arti=dataArti, titulo="Núm Orden", buscado=orden)
			else:
				flash("no existe el registro")
		elif "eliminar" in request.form["Cancelar"]:
			boton, orde = request.form["Cancelar"].split(".")
			try:
				dataS = Salidas.query.filter_by(ordenCompra = orde).one()
				dataArtiS = Salida_Articulos.query.filter_by(salidas_id=dataS.id).all()
				dataE = Entrada.query.filter_by(ordenCompra = orde).one()
				dataArtiE = Articulos.query.filter_by(entradas_id=dataE.id).all()
				##################################################################
				############ borro salidas y salidas articulos ###################
				############ agrego los datos a la tabla entrada #################
				##################################################################
				agr=0
				for item in dataArtiE:
					saldo = float(item.cantidad)
					agregar = float(dataArtiS[agr].cantidad)
					totalA=saldo+agregar
					total = float(totalA) * float(item.p_unit)
					dataArtiE = Articulos.query.filter_by(imtemId=dataArtiS[agr].imtemId).filter_by(ordenCompra=dataArtiS[agr].ordenCompra).one()
					dataArtiE.cantidad=totalA
					dataArtiE.total=total
					inven = Inventario.query.filter_by(id_item=dataArtiS[agr].imtemId).filter_by(orden_compra=dataArtiS[agr].ordenCompra).one()
					cantInve = float(inven.cant_exist) + float(agregar)
					inven.cant_exist = cantInve
					db.session.commit()
					agr+=1
				for item in dataArtiS:
					daS = Salida_Articulos.query.get(item.id)
					db.session.delete(daS)
					db.session.commit()
				dadS = Salidas.query.get(dataS.id)
				db.session.delete(dadS)
				db.session.commit()
				##################################################################
			except Exception as e:
				print (e)
			else:
				flash("el registro se encuentra dañado")
	return render_template("correcionSD.html", nombre=nombre)


@app.route('/correcciones/salidas/parciales', methods=['GET','POST'])
def cancelaMix():
	nombre = session['username']
	form = form_consul_entrada(request.form)
	if request.method == 'POST':
		choice = request.form.get('optradio')
		orden = form.nOrden.data
		if request.form["addOrdenSal"] == "buscarOrd":
			if choice == "1":
				if "-" in orden:
					flash("Utilice el formato de fecha dd/mm/yyyy")
				elif "/" in orden:
					print(len(orden))
					if len(orden)!=10:
						flash(" la fecha {} que introdujo esta incorrecta".format(orden))
					else:
						d,m,a = orden.split('/')
						if len(a)==2:
							an ="20" + a
						elif len(a)==4:
							an = a
						orden = an +"-"+m+"-"+d
						canSal = Salidas.query.filter_by(fecha=orden).all()
						return render_template("cancelaMix.html", nombre=nombre, form=form, titulo="fecha", buscado=orden, data=canSal)
			elif choice == "2":
				if orden:
					canSal = Salida_Articulos.query.filter(Salida_Articulos.descripcion.like("%"+orden+"%")).all()
					return render_template("cancelaMix.html", nombre=nombre, form=form, titulo="Articulo", buscado=orden, data=canSal)
			elif choice == "3":
				if orden:
					canSal = Salidas.query.filter(Salidas.solicitante.like("%"+orden+"%")).all()
					return render_template("cancelaMix.html", nombre=nombre, form=form, titulo="Nombre Recibe", buscado=orden, data=canSal)
			elif choice == "4":
				if orden:
					canSal = Salidas.query.filter_by(oSolicitnte=orden).all()
					return render_template("cancelaMix.html", nombre=nombre, form=form, titulo="Oficio", buscado=orden, data=canSal)
			elif choice == "5":
				if orden:
					canSal = Salidas.query.filter_by(fol_entrada=orden).all()
					return render_template("cancelaMix.html", nombre=nombre, form=form, titulo="Folio", buscado=orden, data=canSal)
		elif "eliminar" in  request.form["addOrdenSal"]:
			if "H" in request.form["addOrdenSal"]:
				e, folio = request.form["addOrdenSal"].split(".")
				xArti=0
			else:
				e, folio = request.form["addOrdenSal"].split(".")
				xArti = 1
			try:
				if xArti == 1 :
					querySalida = Salidas.query.filter_by(id = folio).one()
					histo = Historia.query.filter_by(salida=querySalida.id).all()
				else:
					querySalida = Salidas.query.filter_by(fol_entrada = folio).one()
					histo = Historia.query.filter_by(salida=querySalida.id).all()
				
				##################################################################
				############ borro salidas y salidas articulos ###################
				############ agrego los datos a la tabla entrada #################
				##################################################################
				for item in histo:
					salArti = Salida_Articulos.query.filter_by(id=item.salida_articulos).one()
					if item.entrada_articulos == "Stock": 
						agregar = float(salArti.cantidad)
					else:
						entArti = Articulos.query.filter_by(id=item.entrada_articulos).one()
						saldo = float(entArti.cantidad)
						agregar = float(salArti.cantidad)
						totalA=saldo+agregar
						total = float(totalA) * float(entArti.p_unit)
					inven = Inventario.query.filter_by(id=item.inv).one()
					cantInve = float(inven.cant_exist) + float(agregar)
					inven.cant_exist = cantInve
					db.session.commit()
					print(item.salida_articulos)
					daS = Salida_Articulos.query.get(item.salida_articulos)
					db.session.delete(daS)
					db.session.commit()
				dadS = Salidas.query.get(querySalida.id)
				print(dadS)
				db.session.delete(dadS)
				db.session.commit()
				##################################################################
				flash("La Salida {} se realizó con éxito". format())
			except Exception as e:
				print (e)
			else:
				flash("el registro se encuentra dañado")
	return render_template("cancelaMix.html", nombre=nombre, form=form)


@app.route('/consultayreportes/saldoseninventariofisico', methods=['GET','POST'])
def saldosInvFis():
	nombre = session['username']
	saldo = Inventario.query.filter(Inventario.cant_exist>0).all()
	return render_template("inventarios.html", nombre=nombre, saldo=saldo)


@app.route('/consultayreportes/articulosconexistenciasminimas', methods=['GET','POST'])
def artCExisMin():
	nombre = session['username']
	saldo = Inventario.query.filter(Inventario.cant_exist>0).filter(Inventario.cant_exist<20).group_by(Inventario.id_prod).group_by(Inventario.actividad).all()
	return render_template("inventarios.html", nombre=nombre, saldo=saldo)


@app.route('/consultayreportes/actualizaciondearticulos', methods=['GET', 'POST'])
def actualizaProd():
	nombre = session['username']
	form = formbuscap(request.form)
	if request.method == 'POST':
		ArtCodigo = form.product_id.data
		ArtName = form.product_name.data
		print(request.form['addsalida'])
		if 'buscar' in request.form['addsalida']:
			#Buscar por codigo
			if ArtCodigo:
				print("buscar x codigo")
				pxn = ArtCodigo
				buscapxn = Inventario.query.filter(or_(Inventario.id_item==pxn, Inventario.id_prod==pxn)).filter(Inventario.cant_exist>0).all()
				print(buscapxn)
				return render_template("actProd.html", nombre=nombre, form=form, listatemp=buscapxn, productpxn=ArtCodigo)
			elif ArtName:
				print("buscar x Nombre")
				#Buscar por nombre
				pxn='%'+ArtName+'%'
				#print(LocalName)
				buscapxn = db.session.query(Inventario).filter(Inventario.nom_prod.like('%'+ArtName+'%')).filter(Inventario.cant_exist>0).all()
				return render_template("actProd.html", nombre=nombre, form=form, listatemp=buscapxn, productpxn=ArtName)
			else:
				flash("Debe elegir un articulo")
				return render_template("buscar.html", nombre=nombre, form=form_buscap,listatemp2=session['listatotal'])
	return render_template("actProd.html", nombre=nombre, form=form)


@app.route("/modiProd/<int:numInv>", methods=['GET', 'POST'])
def modiProd(numInv):
	nombre = session['username']
	consulta = Inventario.query.filter(Inventario.id==numInv).one()
	form = formActInven(formdata=request.form, obj=consulta)
	if request.method == 'POST' and form.validate():
		consulta.nom_interno = form.nom_interno.data.upper()
		consulta.descripcion = form.descripcion.data.upper()
		consulta.id_familia = form.id_familia.data.upper()
		consulta.procedencia = form.procedencia.data.upper()
		consulta.f_recepcion = form.f_recepcion.data.upper()
		db.session.commit()
		flash("El regsitro se Modifico con Exito, el estante es {}". format(str(form.procedencia.data)))
		return redirect(url_for("actualizaProd"))
	return render_template("modiProd.html", form=form, nombre=nombre)


@app.route('/consultayreportes/entradasAlmacen', methods=['GET', 'POST'])
def listaEntradas():
	nombre = session['username']
	saldo=[]
	if request.method == 'POST':
		mes = request.form.get('mes')
		anio = request.form.get('anio')
		i=1
		saldo=[]
		query = Entrada.query.filter(extract( "year", Entrada.fecha) == anio).filter(extract("month", Entrada.fecha) == mes).all()
		for i in range(len(query)):
			query2 = Articulos.query.filter(Articulos.entradas_id==query[i-1].id).order_by(Articulos.entradas_id).all()
			saldo.append(query2)
	return render_template("listaEntradas.html", nombre=nombre, saldo=saldo)


@app.route('/consultayreportes/salidasAlmacen', methods=['GET', 'POST'])
def listaSalidas():
	nombre = session['username']
	saldo=[]
	if request.method == 'POST':
		mes = request.form.get('mes')
		anio = request.form.get('anio')
		i=1
		saldo=[]
		query = Salidas.query.filter(extract( "year", Salidas.fecha) == anio).filter(extract("month", Salidas.fecha) == mes).all()
		for i in range(len(query)):
			query2 = Salida_Articulos.query.filter(Salida_Articulos.salidas_id==query[i-1].id).order_by(Salida_Articulos.salidas_id).all()
			saldo.append(query2)
	return render_template("listaSalidas.html", nombre=nombre, saldo=saldo)


@app.route('/consultayreportes/inventarioFisico', methods=['GET', 'POST'])
def listaInventario():
	nombre = session['username']
	listaSalidas=[]
	totalEntradas=[]
	saldo=[]
	queryInvEntra=[]
	queryInvStock=[]
	if request.method == 'POST':
		if 'enviar' in request.form['guardar']:
			session['mes'] = request.form.get('mes')
			mes = request.form.get('mes')
			session['anio'] = request.form.get('anio')
			anio = request.form.get('anio')

			###### Listado de Salidas correspondiente al periodo solicitado ##########
			querySalidas = Salidas.query.filter(extract( "year", Salidas.fecha) < anio).all() + Salidas.query.filter(extract( "year", Salidas.fecha) == anio).filter(extract( "month", Salidas.fecha)==mes).all()

			for item in querySalidas:
				query3 = Salida_Articulos.query.filter(Salida_Articulos.salidas_id==item.id).order_by(Salida_Articulos.salidas_id).all()
				listaSalidas.append(query3)
			##########################################################################

			###### Listado de Entradas correspondiente al periodo solicitado ##########
			queryEntradas = Entrada.query.filter(extract( "year", Entrada.fecha) < anio).all() + Entrada.query.filter(extract( "year", Entrada.fecha) == anio).filter(extract( "month", Entrada.fecha) <= mes).all()

			for item in (queryEntradas):
				query2 = Articulos.query.filter(Articulos.entradas_id==item.id).order_by(Articulos.entradas_id).all()
				totalEntradas.append(query2)
			###########################################################################
			
			############### Inventario de Stock #######################################	
			queryInvStock = Inventario.query.filter(Inventario.cant_dispon > 0).filter_by(actividad ='a').order_by(Inventario.id_item).all()
			###########################################################################

			
			############### inventario de todo lo que se modifico con entradas ########
			queryInvEntra = Inventario.query.filter_by(actividad = "Entrada").all() + Inventario.query.filter_by(actividad = "Surtido").all() + Inventario.query.filter_by(actividad = "PSurtido").all()
			###########################################################################

			
			#########################################
			##########  Comienza la Magia  ##########
			#########################################
			n=0
			for item in totalEntradas:
				for i in item:
					if i.codigo == queryInvEntra[n].id_prod:
						if (i.p_unit) == (queryInvEntra[n].costo_unit):
							queryInvEntra[n].cant_dispon=(queryInvEntra[n].cant_dispon)+i.cantidad
							n+=1

			n=0
			for item in listaSalidas:
				for i in item:
					if i.codigo == queryInvEntra[n].id_prod and queryInvEntra[n].cant_dispon > 0:
						if (i.p_unit) == (queryInvEntra[n].costo_unit):
							queryInvEntra[n].cant_dispon = (queryInvEntra[n].cant_dispon)-(i.cantidad)
							n+=1
					else:
						if (i.p_unit) == (queryInvEntra[n+1].costo_unit):
							queryInvEntra[n+1].cant_dispon= (queryInvEntra[n+1].cant_dispon)-(i.cantidad)
							n+=2
			saldo = queryInvEntra+queryInvStock
		elif 'imprimir' in request.form['guardar']:
			mes = session['mes']
			anio = session['anio']
			###### Listado de Salidas correspondiente al periodo solicitado ##########
			querySalidas = Salidas.query.filter(extract( "year", Salidas.fecha) < anio).all() + Salidas.query.filter(extract( "year", Salidas.fecha) == anio).filter(extract( "month", Salidas.fecha)==mes).all()

			for item in querySalidas:
				query3 = Salida_Articulos.query.filter(Salida_Articulos.salidas_id==item.id).order_by(Salida_Articulos.salidas_id).all()
				listaSalidas.append(query3)
			##########################################################################

			###### Listado de Entradas correspondiente al periodo solicitado ##########
			queryEntradas = Entrada.query.filter(extract( "year", Entrada.fecha) < anio).all() + Entrada.query.filter(extract( "year", Entrada.fecha) == anio).filter(extract( "month", Entrada.fecha) <= mes).all()

			for item in (queryEntradas):
				query2 = Articulos.query.filter(Articulos.entradas_id==item.id).order_by(Articulos.entradas_id).all()
				totalEntradas.append(query2)
			###########################################################################
			
			############### Inventario de Stock #######################################	
			queryInvStock = Inventario.query.filter(Inventario.cant_dispon > 0).filter_by(actividad ='a').order_by(Inventario.id_item).all()
			###########################################################################

			
			############### inventario de todo lo que se modifico con entradas ########
			queryInvEntra = Inventario.query.filter_by(actividad = "Entrada").all() + Inventario.query.filter_by(actividad = "Surtido").all() + Inventario.query.filter_by(actividad = "PSurtido").all()
			###########################################################################

			
			#########################################
			##########  Comienza la Magia  ##########
			#########################################
			n=0
			for item in totalEntradas:
				for i in item:
					if i.codigo == queryInvEntra[n].id_prod:
						if (i.p_unit) == (queryInvEntra[n].costo_unit):
							queryInvEntra[n].cant_dispon= queryInvEntra[n].cant_dispon + i.cantidad
							n+=1
			n=0
			for item in listaSalidas:
				for i in item:
					if i.codigo == queryInvEntra[n].id_prod and queryInvEntra[n].cant_dispon > 0:
						if (i.p_unit) == (queryInvEntra[n].costo_unit):
							queryInvEntra[n].cant_dispon= (queryInvEntra[n].cant_dispon) - i.cantidad
							n+=1
					else:
						if (i.p_unit) == (queryInvEntra[n+1].costo_unit):
							queryInvEntra[n].cant_dispon= (queryInvEntra[n].cant_dispon) - i.cantidad
							n+=2
			saldo = queryInvEntra+queryInvStock
			return InventarioQuery(saldo,"Listado entradas de Almacen")
	return render_template("listaInventario.html", nombre=nombre, saldo= saldo)


if __name__ == '__main__':
    crsf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=8000, host='0.0.0.0')