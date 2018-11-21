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
from forms import Create_Form, LoginForm, formbuscap, formbuscaentrada
import os
import pypyodbc 
from bs4 import BeautifulSoup
from flask_wtf import CSRFProtect


app = Flask(__name__)
app.secret_key = "my_secret_key"
crsf = CSRFProtect()
#app.config.from_object(DevelopmentConfig)

#################################################
# CONEXION A SQL SERVER 2012
# Creo la cadena de conexion 
connection = pypyodbc.connect('Driver={SQL Server};Server=.;Database=capaPrueba;uid=sa;pwd=12345')

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
listatotal = []  # lista global que contendra los articulos para e/s
bolsa = [] # lista donde se encuentra el producto buscado y que ira llenando la listatotal
Localizado2 = []
Localizado  = []
####################################################

@app.before_request
def before_request():
	if 'username' not in session and request.endpoint in ['index', 'entradas', 'buscaprod', 'verlista_']:
		return redirect(url_for('login'))
	elif 'username' in session:
		usr = session['username']
		if request.endpoint in ['login']:
			return redirect(url_for('index'))


# Paso en la url un nombre de usuario
@app.route("/index/")
@app.route("/")
def index():
	if 'username' in session:
		nombre = session['username'].upper()
		return render_template("menualm.html",nombre=nombre)
	else:
		return. redirect(url_for('login'))


@app.route('/entradas', methods=['GET', 'POST'])	
def entradas():
	nombre = session['username'].upper()
	form_buscaentrada = formbuscaentrada(request.form)
	if request.method == 'POST':
		if 'buscar' in request.form['addentrada']:
			print('Entradas-Boton buscar funcionando')
	else:
		print("Entradas-No entro al método POST")
	return render_template("entradasalm.html",form=form_buscaentrada,nombre=nombre)
	
	
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
		buscaUser = """SELECT * FROM USER_LOGIN WHERE USER_LOGIN_ID ='%s'"""%username
		cursor.execute(buscaUser)
		Found = cursor.fetchall()
		#Buscamos en el cursor los primeros dos campos que contienen usuario y contraseña
		for row in Found:
		    username_ = row[0] # usuario
		    password_ = row[1] # contraseña
		    print(username_)
		    print(password_)
		if username_ and password == password_ :
			sucess_message = 'Bienvenido {}'.format(username)
			flash(sucess_message)
			session['username'] = username
			return redirect(url_for('index'))
		else:
			error_message = '{} No es un usuario del sistema'.format(username)
			flash(error_message)
			return redirect(url_for('login'))
	return render_template('loginalm.html', form = login_form)


@app.route('/logout')
def logout():
	if 'username' in session:
		connection.close()
		session.pop('username')		    
	return redirect(url_for('login'))

	
@app.route('/buscaprod', methods=['GET', 'POST'])
def buscaprod():
	global bolsa
	global listatotal
	Localizado = []
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
						if item in fila:
							print("Borrando tupla que contenga el elemento:" + item)
							listatotal.pop(pos)
							break
						else:
							print("No esta el elemento:" + item)
					pos += 1					
			print(listatotal)
			verlista =  True
			return render_template('buscaprod.html',form=form_buscap,listaglobal=listatotal,verlista=verlista)
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
							if item in fila:
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
			return render_template('buscaprod.html',form=form_buscap,lista=lista,listaglobal=listatotal)
		
		if 'agregar' in request.form['addsalida']:
			global Localizado
			valor_chkpxn = request.form.getlist('chklista0')
			if valor_chkp == []:
				 error_message = '¡ATENCION! No se agrego ningún producto'
				 flash(error_message)
			else:
				print("A ver si existe Localizado")
				print(Localizado)
				for item in valor_chkp:
					pos = 0
					for fila in Localizado:
						for col in fila:
							if item in fila:
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
			return render_template('buscaprod.html',form=form_buscap,lista=lista,listaglobal=listatotal)

		if 'agregar_2' in request.form['addsalida']:
			print("entro a añadir producto a la lista")              
			listatotal.append(bolsa)
			print(listatotal)
			return render_template('buscaprod.html',form=form_buscap,lista=lista,listaglobal=listatotal)

		elif 'buscaotro' in request.form['addsalida']:
			print( 'agregar otro producto')
			return render_template('buscaprod.html',form=form_buscap,listaglobal=listatotal)

		elif 'versalida' in request.form['addsalida']:
			print('Listado total de productos')
			if listatotal == []:
				error_message = '¡ATENCION! No hay productos en la lista'
				flash(error_message)
			print(listatotal)
			return render_template('buscaprod.html',form=form_buscap,listaglobal=listatotal)
			#return render_template('buscaprod.html',form=form_buscap,lista=lista,listaglobal=listatotal)

		elif 'borrarsalida' in request.form['addsalida']:
			listatotal.clear()
			return render_template('buscaprod.html',form=form_buscap,lista=lista,listaglobal=listatotal)	

		elif 'buscar' in request.form['addsalida']:
			print('Buscando producto')
			product_id = form_buscap.product_id.data
			product_name = form_buscap.product_name.data
			product_name = product_name.strip()
			print("el metodo es: " + request.method)
			#product_id = request.form['product_id']
			print("Product_id es:" + product_id)
			print("Product_name es:" + product_name)
			#Creamos la consulta
			pxn='%'+product_name+'%'
			if product_id:
				print("Entro a Product_id ")
				#buscap = """SELECT * FROM PRODUCT WHERE PRODUCT_ID ='%s'"""%product_id
				#buscap = ("SELECT a.PRODUCT_ID,INTERNAL_NAME,QUANTITY_ON_HAND_TOTAL,QUANTITY_UOM_ID,AVAILABLE_TO_PROMISE_TOTAL FROM PRODUCT a, INVENTORY_ITEM b WHERE a.PRODUCT_ID = %sproduct_id AND  b.PRODUCT_ID= %sproduct_id")				
				buscap = """SELECT  a.PRODUCT_ID,INTERNAL_NAME,QUANTITY_ON_HAND_TOTAL,QUANTITY_UOM_ID,AVAILABLE_TO_PROMISE_TOTAL, UNIT_COST,INVENTORY_ITEM_ID FROM PRODUCT a INNER JOIN INVENTORY_ITEM b ON a.PRODUCT_ID =  b.PRODUCT_ID  AND a.PRODUCT_ID='%s'"""%(product_id)
				cursor.execute(buscap)
				Localizado = cursor.fetchall()
				Localizado2 = []
				print("Imprimo consulta de  Product_id ")
				print(Localizado)
			elif product_name:
				print("Entro a Product_name ")
				buscapxn = """SELECT PRODUCT.PRODUCT_ID,INTERNAL_NAME,QUANTITY_ON_HAND_TOTAL,QUANTITY_UOM_ID,AVAILABLE_TO_PROMISE_TOTAL,UNIT_COST,INVENTORY_ITEM_ID FROM PRODUCT,INVENTORY_ITEM WHERE PRODUCT_NAME LIKE '%s' AND PRODUCT.PRODUCT_ID = INVENTORY_ITEM.PRODUCT_ID"""%pxn
				#buscapxn = """SELECT PRODUCT_ID, PRODUCT_TYPE_ID, INTERNAL_ID, FAMILIA_ID FROM PRODUCT WHERE PRODUCT_ID ='%s'"""%product_id
				cursor.execute(buscapxn)
				Localizado2 = cursor.fetchall()	
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
				return render_template('buscaprod.html',form=form_buscap,lista=Localizado,listaglobal=listatotal)

			if Localizado2: # Si la busqueda obtuvo exito x nombre del producto
				for row in Localizado2:
			           #result_ = row[10] # descripcion
			           #lista=(row[0], row[1], row[10], row[81])
			           #print(result_)	
			           #bolsa = lista
			         print("Listado de la consulta x nombre")	
			         print(Localizado2)	
			         return render_template('buscaprod.html',form=form_buscap ,listapxn=Localizado2,listaglobal=listatotal,productpxn=product_name)
			else:
				 error_message = 'El producto: '+'{} no existe'.format(product_id)
				 flash(error_message)
				 print(result_)
		else:
			flash('No se encuentra la opcion del boton')
			return render_template('buscaprod.html',form=form_buscap)
	else:
		 print("No entro al metodo POST")		
	return render_template('buscaprod.html',form=form_buscap,listaglobal=listatotal)
		
	
@app.route('/verlista_', methods=['GET', 'POST'])
def verlista_():	
	return render_template('ver_listaprod.html',listaglobal=listatotal)

	
if __name__== "__main__":
		app.run()
	