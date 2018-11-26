import pymssql #SQLServer

import pymysql  #MySQL
pymysql.install_as_MySQLdb()
import pymysql.cursors


server = "DESKTOP-TRVGHH8\\SQLHUGO" 
user = "sa"
password="12345"
base="capa"


### Conector SQLServer
connection = pymssql.connect(host=server, user=user, password=password, database=base)

try :
	##### cursor para SQL Server
	SQLcursor = connection.cursor()
	print("Conexion SQLServer establecida con exito")
except:
	print("No hay Conexion a SQL SERVER") 


##### Conector MySQL
connmysql = pymysql.connect(host="localhost", user="root", password="", db="almacen")

try:
	##### Cursor MySQL
	cursorMysql= connmysql.cursor()
	print("Conexiona Mysql Exitosa")
except:
	print("FAllo la conexion a MySQL")


query = """Select a.product_id as id_item from PRODUCT a INNER JOIN INVENTORY_ITEM b ON a.PRODUCT_ID =  b.PRODUCT_ID"""
SQLcursor.execute(query)
for item in SQLcursor.fetchall():
	print (item)
