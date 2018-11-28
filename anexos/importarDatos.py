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

x=tuple
query = """select * from postal_address"""
SQLcursor.execute(query)
query2="""INSERT INTO proveedores(`CONTACT_MECH_ID`, `TO_NAME`, `ATTN_NAME`, `ADDRESS1`, `ADDRESS2`, `DIRECTIONS`, `CITY`, `POSTAL_CODE`, `POSTAL_CODE_EXT`, `COUNTRY_GEO_ID`, `STATE_PROVINCE_GEO_ID`, `COUNTY_GEO_ID`, `POSTAL_CODE_GEO_ID`, `GEO_POINT_ID`, `LAST_UPDATED_STAMP`, `LAST_UPDATED_TX_STAMP`, `CREATED_STAMP`, `CREATED_TX_STAMP`, `MUNICIPALITY_GEO_ID`, `BANCO_ID`, `NUMERO_CUENTA`, `CLABE_INTERBANCARIA`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
for item in SQLcursor.fetchall():
	x=(str(item[0]),str(item[1]),str(item[2]),str(item[3]),str(item[4]),str(item[5]),str(item[6]),str(item[7]),str(item[8]),str(item[9]),str(item[10]),str(item[11]),str(item[12]),str(item[13]),str(item[14]),str(item[15]),str(item[16]),str(item[17]),str(item[18]),str(item[19]),str(item[20]),str(item[21]))
	try:
		cursorMysql.execute(query2, x)
	except Exception as e:
		print(e)