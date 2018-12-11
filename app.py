# Sistema web para la gestión del Almacén General de la CAPA
#Programador: Cesar Herrera Mut ( Septiembre de 2018)
#Analista Profesional - Dirección de Informática - Direccion General
#Desarrollado en Python 3.4
#Si no logro terminarlo en diciembre va rodar mi cabeza :7 :/ 
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
from forms import Create_Form, LoginForm, formbuscap, formbuscaentrada, form_salida_orden, form_consul_entrada
import os
from models import db, User, Inventario, Articulos, Entrada

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
##################################################

######## Variables Globales ########################
global Localizado2
global Localizado
global Cantidades
listatotal = []  # lista global que contendra los articulos para e/s
bolsa = [] # lista donde se encuentra el producto buscado y que ira llenando la listatotal
Localizado2 = []
Localizado  = []
Cantidades  = []
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
	if 'username' not in session and request.endpoint in ['index', 'entradas', 'buscaprod', 'verlista_']:
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
	
	
@app.route('/salidas', methods=['GET', 'POST'])	
def salidas():
	nombre = session['username'].upper()
	form_buscaentrada = formbuscaentrada(request.form)
	if request.method == 'POST':
		id_orden = form_buscaentrada.order_id.data
		if 'buscar' in request.form['addentrada']:
			print('Salidas-Boton buscar funcionando')			
			orden = """SELECT * FROM entradas a INNER JOIN entradaarticulos b ON a.ordencompra = b.ordencompra  WHERE a.ordencompra='%s'"""%(id_orden)
			total_o= """SELECT sum( total ) FROM entradaarticulos WHERE ordencompra = '%s'"""%(id_orden)
			det_orden = db.session.execute(orden).fetchall()
			total_ord = db.session.execute(total_o).fetchall()
			if det_orden:
				print("RESULTADO DE LA CONSULTA POR ORDEN")
				print(det_orden)
				print("IMPRIMO LAS FILAS")
				print("total de la orden")
				print(total_ord[0])
				for fila in det_orden:
					print(fila)
			else:
				print("NINGUN RESULTADO DE LA ORDEN:"+id_orden)
	else:
		print("Salidas-No entro al método POST")
	return render_template("salidas.html", form=form_buscaentrada, nombre=nombre)
	
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	username_ =""
	password_ =""
	login_form = LoginForm(request.form) 
	if request.method == 'POST' and login_form.validate() :
		username = login_form.username.data
		password = login_form.password.data
		print(username)
		print(password)
		user = User.query.filter_by(username=username).first()
		#Buscamos en el cursor los primeros dos campos que contienen usuario y contraseña
		if user is not None and user.verify_password(password):
			sucess_message = 'Bienvenido {}'.format(username)
			flash(sucess_message)
			session['username'] = username
			return redirect(url_for('index'))
		else:
			error_message = '{} No es un usuario del sistema'.format(username)
			flash(error_message)
			return redirect(url_for('login'))
	return render_template('login.html', form = login_form)


@app.route('/logout')
def logout():
	if 'username' in session:
		connection.close()
		session.pop('username')		    
	return redirect(url_for('login'))

	
@app.route('/buscaprod', methods=['GET', 'POST'])
def buscaprod():
	nombre = session['username'].upper()
	global bolsa
	global listatotal
	lista = []
	print("inicio...")
	result_ = "Fallo la busqueda"
	form_buscap = formbuscap(request.form)
	if request.method == 'POST':
		print('Entrando a POST')
		if 'enviar' in request.form['addsalida']:
			print("Aqui debo validar los objetos borrar con el valor del producto para crear una nueva listaglobal") 
			valor_chklista = request.form.getlist('chklista')
			print(valor_chklista)
			for item in valor_chklista:
				pos = 0 
				for fila in listatotal:
					for col in fila:
						# Para SQL Server es: if item in fila:
						# Para MYSQL Server es: if item == fila:
						if item == col:
							print("Borrando tupla que contenga el elemento:" + item)
							listatotal.pop(pos)
							break
						else:
							print("No esta el elemento:" + item)
					pos += 1					
			print(listatotal)
			verlista =  True
			return render_template('buscaprod.html',form=form_buscap,listaglobal=listatotal,verlista=verlista, nombre=nombre)
		if 'agregarpxn' in request.form['addsalida']:
			global Localizado2
			valor_chkpxn = request.form.getlist('chkpxn')
			if valor_chkpxn == []:
				 error_message = '¡ATENCION! No se agrego ningún producto'
				 flash(error_message)
			else:
				print("A ver si existe Localizado2")
				print(Localizado2)
				for item in valor_chkpxn:
					pos = 0
					for fila in Localizado2:
						for col in fila:
							# Para SQL Server es: if item in fila:
						    # Para MYSQL Server es: if item == fila:
							if item == col:
								print("Si esta en Localizado2")
								a = fila
								listatotal.append(a)
								sucess_message = '¡ATENCION! El producto se agrego correctamente'
								flash(sucess_message)
								print(pos)
								print(a)
								break
							else:
								print(" NO esta en localizado2")
						pos += 1							
			print("entro a añadir producto a la lista x nombre")              
			#listatotal.append(bolsa)
			print(valor_chkpxn)
			return render_template('buscaprod.html',form=form_buscap,lista=lista,listaglobal=listatotal, nombre=nombre)
		
		if 'agregar' in request.form['addsalida']:
			print("If agregar in request.form['addsalida']:")
			global Localizado
			global Localizado3
			valor_chkp = request.form.getlist('chklista0')
			if valor_chkp == []:
				 error_message = '¡ATENCION! No se agrego ningún producto'
				 flash(error_message)
			else:
				print("A ver si existe Localizado MYSQL")
				print(Localizado)
				print("Localizado3 SQL server")
				print(Localizado3)
				print(valor_chkp)
				for item in valor_chkp:
					pos = 0
					for fila in Localizado:
						print("Imprimo Fila")
						print(fila)
						for col in fila:
							print("Imprimo Columnna")
							print(col)
							#Para Sql Server es : if item in fila:
							#Para MySql es if item == col:
							if item == col:
								print("Imprimo item")
								print(item)
								print("Si esta en Localizado")
								a = fila
								listatotal.append(a)
								sucess_message = '¡ATENCION! El producto se agrego correctamente'
								flash(sucess_message)
								print(pos)
								print(a)
								break
							else:
								print(" NO esta en localizado")
						pos += 1							
			print("entro a añadir producto a la lista x Clave")              
			#listatotal.append(bolsa)
			print(valor_chkp)
			return render_template('buscaprod.html',form=form_buscap,lista=lista,listaglobal=listatotal, nombre=nombre)

		if 'agregar_2' in request.form['addsalida']:
			print("entro a añadir producto a la lista")              
			listatotal.append(bolsa)
			print(listatotal)
			return render_template('buscaprod.html',form=form_buscap,lista=lista,listaglobal=listatotal, nombre=nombre)

		elif 'buscaotro' in request.form['addsalida']:
			print( 'agregar otro producto')
			return render_template('buscaprod.html',form=form_buscap,listaglobal=listatotal, nombre=nombre)

		elif 'versalida' in request.form['addsalida']:
			print('Listado total de productos')
			if listatotal == []:
				error_message = '¡ATENCION! No hay productos en la lista'
				flash(error_message)
			print(listatotal)
			return render_template('buscaprod.html',form=form_buscap,listaglobal=listatotal, nombre=nombre)
			#return render_template('buscaprod.html',form=form_buscap,lista=lista,listaglobal=listatotal)

		elif 'borrarsalida' in request.form['addsalida']:
			listatotal.clear()
			return render_template('buscaprod.html',form=form_buscap,lista=lista,listaglobal=listatotal, nombre=nombre)	

		elif 'buscar' in request.form['addsalida']:
			print('Buscando producto')
			product_id = form_buscap.product_id.data
			product_name = form_buscap.product_name.data
			product_name = product_name.strip()
			print("el metodo es: " + request.method)
			#product_id = request.form['product_id']
			print("Product_id es:" + product_id)
			print("Product_name es:" + product_name)
			busca_pr = """SELECT  id_prod,nom_prod,cant_exist,um,cant_dispon,costo_unit,id_item FROM inventario  WHERE id_prod='%s'"""%(product_id)
			prod_tmp = db.session.execute(busca_pr).fetchall()

			#prod_tmp = inventario.query.filter_by(id_prod=product_id).all()
			if prod_tmp is None:
				print("No hay productos en mysql")
			elif prod_tmp:
				print("Productos de mysql")
				print(prod_tmp)
			#Creamos la consulta
			pxn='%'+product_name+'%'
			if product_id:
				print("Entro a Product_id ")
				#buscap = """SELECT * FROM PRODUCT WHERE PRODUCT_ID ='%s'"""%product_id
				#buscap = ("SELECT a.PRODUCT_ID,INTERNAL_NAME,QUANTITY_ON_HAND_TOTAL,QUANTITY_UOM_ID,AVAILABLE_TO_PROMISE_TOTAL FROM PRODUCT a, INVENTORY_ITEM b WHERE a.PRODUCT_ID = %sproduct_id AND  b.PRODUCT_ID= %sproduct_id")				
				buscap3 = """SELECT  a.PRODUCT_ID,INTERNAL_NAME,QUANTITY_ON_HAND_TOTAL,QUANTITY_UOM_ID,AVAILABLE_TO_PROMISE_TOTAL, UNIT_COST,INVENTORY_ITEM_ID FROM PRODUCT a INNER JOIN INVENTORY_ITEM b ON a.PRODUCT_ID =  b.PRODUCT_ID  AND a.PRODUCT_ID='%s'"""%(product_id)
				buscap = """SELECT  id_prod,nom_prod,cant_exist,um,cant_dispon,costo_unit,id_item FROM inventario  WHERE id_prod='%s'"""%(product_id)
				cursor.execute(buscap3)
				Localizado = db.session.execute(buscap).fetchall()
				Localizado3 = cursor.fetchall()
				Localizado2 = []

				print("Imprimo consulta de  Product_id ")
				print(Localizado)
			elif product_name:
				print("Entro a Product_name ")
				#buscapxn = """SELECT PRODUCT.PRODUCT_ID,INTERNAL_NAME,QUANTITY_ON_HAND_TOTAL,QUANTITY_UOM_ID,AVAILABLE_TO_PROMISE_TOTAL,UNIT_COST,INVENTORY_ITEM_ID FROM PRODUCT,INVENTORY_ITEM WHERE PRODUCT_NAME LIKE '%s' AND PRODUCT.PRODUCT_ID = INVENTORY_ITEM.PRODUCT_ID"""%pxn
				buscapxn = """SELECT id_prod,nom_prod,cant_exist,um,cant_dispon,costo_unit,id_item FROM inventario WHERE nom_prod LIKE '%s' """%pxn
				#buscapxn = """SELECT PRODUCT_ID, PRODUCT_TYPE_ID, INTERNAL_ID, FAMILIA_ID FROM PRODUCT WHERE PRODUCT_ID ='%s'"""%product_id
				#cursor.execute(buscapxn)
				#Localizado2 = cursor.fetchall()	
				Localizado2 = db.session.execute(buscapxn).fetchall()
				print("Imprimo consulta por Nombre ")
				print(Localizado2)
				Localizado = []
			#Tabla sicopa PRODUCT_ID,  campo llave			
			if Localizado:
				print("Imprimo consulta de  Product_id entrando al If Localizado ")

				# Si la busqueda obtuvo exito x codigo del producto
				#for row in Localizado:
					#print("Entro a localizado e imprimo la consulta")
				print(Localizado)
					#result_ = row[1] # descripcion
					#lista=(row[0], row[1], row[2], row[3])
					#print(result_)
					#bolsa = lista
					#print("Producto buscado por codigo")
					#print(bolsa)
				return render_template('buscaprod.html',form=form_buscap,lista=Localizado,listaglobal=listatotal, nombre=nombre)

			if Localizado2: # Si la busqueda obtuvo exito x nombre del producto
				for row in Localizado2:
			           #result_ = row[10] # descripcion
			           #lista=(row[0], row[1], row[10], row[81])
			           #print(result_)	
			           #bolsa = lista
			         print("Listado de la consulta x nombre")	
			         print(Localizado2)	
			         return render_template('buscaprod.html',form=form_buscap ,listapxn=Localizado2,listaglobal=listatotal,productpxn=product_name, nombre=nombre)
			else:
				 error_message = '¡ATENCION! El producto: '+'{} no existe'.format(product_id)
				 flash(error_message)
				 print(result_)
		elif 'entrada_alm' in request.form['addsalida']:
				global listatotal
				global Cantidades
				Cantidades = request.form.getlist('cants')
				pos = 0
				print('Insertando elementos dentro de cada lista, (lista de listas)')
				#Convierto la lista de tuplas en lista de listas para poder modificarlos
				listatotal = [list(fila) for fila in listatotal]	
				for item in Cantidades:
					j= listatotal[pos]
					j.append(item)
					pos += 1
					print("Lista final para Entrada")
					print(listatotal)
				return redirect(url_for('EntradaOrden'))

		elif 'salida_alm' in request.form['addsalida']:	
				global listatotal
				cantidades = request.form.getlist('cants')
				print("Lista final para Salida")
				print(listatotal,cantidades)		 
		else:
			flash('No se encuentra la opcion del boton')
			return render_template('buscaprod.html',form=form_buscap)
	else:
		 print("No entro al metodo POST")		
	return render_template('buscaprod.html', form=form_buscap, listaglobal=listatotal, nombre=nombre)
		
	
@app.route('/verlista', methods=['GET', 'POST'])
def verlista():	
	return render_template('verlista.html',listaglobal=listatotal)


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
		elif len(str(folio))< 5:
			flash("El campo {} es requerido".format("Folio"))
		elif len(str(factura))< 1:
			flash("El campo {} es requerido".format("Factura"))
		elif len(str(numFactura))< 1:
			flash("El campo {} es requerido".format("Número de Factura"))
		elif len(str(orden1))< 1:
			flash("El campo {} es requerido".format("Orden de Compra"))
		elif len(str(dep_soli))< 5:
			flash("El campo {} es requerido".format("Departamento Solicitante"))
		elif len(str(nReq))< 1:
			flash("El campo {} es requerido".format("Número de Requerimiento"))
		elif len(str(oSoli))< 5:
			flash("El campo {} es requerido".format("Oficio Solicitante"))
		elif len(str(tCompra))< 5:
			flash("El campo {} es requerido".format("Tipo de Compra"))
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
				for item in listatotal:
					total = float(item[5])*float(item[7])
					arti = Articulos(entradas_id = datos,
						cantidad = item[7],
						udm = item[3],
						codigo = item[0],
						descripcion = item[1],
						p_unit = item[5],
						total = total,
						ordenCompra = orden1,
						imtemId = item[6],)
					db.session.add(arti)
					db.session.commit()
					canti = Inventario.query.filter_by(id_item = item[6]).one()
					print(canti)
					saldo = canti.cant_exist
					print(saldo)
					t = float(item[7])+ float(saldo)
					print(t)
					canti.cant_exist = t
					db.session.commit()
				flash("Entrada Núm {} Realizada con exito".format(datos))
				listas = list()
				listas.append('Proveedor:')
				listas.append('Nombre Comercial:')
				x = entradaPdf("Entrada", listas, generales, listatotal)
				return x
			else:
				flash("La orden núm. {} ya ha sido capturada anteriormente".format(orden1))
	return render_template("entradaOrden.html", nombre=nombre, form=form, listaglobal=listaGlobal(listatotal))


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
	return render_template("consulta.html", nombre=nombre, form=form)

	
if __name__ == '__main__':
    crsf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=8000, host='0.0.0.0')