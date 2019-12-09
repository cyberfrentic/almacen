import os


class Config(object):
    SECRET_KEY = '7897q%3=;8J+X5:f.+pU9e!;6x:E*n_9^Ky0~.R465'

########################################################################################
# CONEXION A MYSQL
# Creo la cadena de conexion 
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://administrador:ha260182ha@192.168.15.45/almacen'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.abspath("static/uploads/")