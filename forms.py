from wtforms import Form
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from wtforms import PasswordField
from wtforms import HiddenField
from wtforms import validators
from wtforms import DateField, DateTimeField, IntegerField, SelectField
from wtforms import DecimalField
from models import User
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from models import db
from models import User, proveedor, data_import_party


def length_honeypot(form, field):
	if len(field.data) > 0:
		raise validators.ValidationError('El Campo debe estar vacio.')


class Create_Form(Form):
    username = StringField('Usuario',
                           [validators.Required(message='El user es requerido!.'),
                            validators.length(min=8, max=20, message='ingrese un username valido!.')
                            ])
    password = PasswordField('Password', [validators.Required(message='El password es Indispensable!.'),
                                          validators.EqualTo('confirm', message='Las contraseñas deben ser iguales')])
    confirm = PasswordField('Repita la Contraseña')
    email = EmailField('Correo electronico',
                       [validators.Required(message='El Email es requerido!.'),
                        validators.Email(message='Ingrese un email valido!.'),
                        validators.length(min=4, max=40, message='Ingrese un email valido!.')
                        ])
    honeypot = HiddenField('', [length_honeypot])

    
def validate_username(form, field):
        username = field.data
        user = User.query.filter_by(username = username).first()
        if user is not None:
            raise validators.ValidationError('El usuario ya existe en la base de datos.')


class LoginForm(Form):
	username = StringField('Usuario',
		[validators.Required(message = 'El Nombre de Usuario es Requerido!.'),
		validators.length(min= 4, max=25, message= 'ingrese un Nombre de Usuario valido!.')
		])
	password = PasswordField('Contraseña', [validators.Required(message='La Contraseña es Requerida!.')])
		

class formbuscap(Form):
    product_id = StringField('',
        [validators.Required(message = 'Debe proporcional la clave del producto!.'),
        validators.length(max = 12, message='El campo debe contener 12 caracteres como máximo')
        ])
    product_name = StringField('',
        [validators.Required(message = 'Nombre aproximado del producto!.'),
        validators.length(max = 60, message='El nombre debe contener una frase completa que describa el producto')
        ])


class formbuscaentrada(Form):
    order_id = StringField('',
        [validators.Required(message = 'Debe proporcional el número de entrada u orden!.'),
        validators.length(max = 12, message='El campo debe contener 12 caracteres como máximo')
        ])

def get_pk(obj): # def necesario para que el QuerySelectField pueda mostrar muchos registros.
    return str(obj)

def prov():
    return db.session.query(proveedor.ATTN_NAME).distinct(proveedor.ATTN_NAME).group_by(proveedor.ATTN_NAME)
   

def departamentos():
    return db.session.query(data_import_party.group_name).distinct(data_import_party.group_name).group_by(data_import_party.group_name)

def prov2():
     return db.session.query(proveedor.TO_NAME).distinct(proveedor.TO_NAME).group_by(proveedor.TO_NAME)
    
class form_salida_orden(Form):
    proveedor = QuerySelectField("", query_factory = prov, get_pk=get_pk, allow_blank=True)
    fecha = DateField('', format='%d/%m/%Y',validators=(validators.Optional(),))
    nomComer = QuerySelectField("", query_factory = prov2, get_pk=get_pk, allow_blank=True)
    folio = IntegerField("", [validators.required()])
    factura = SelectField('', choices=[('', ''), ('F', 'Factura'), ('N', 'Nota'), ("C", 'Cotiación')], )
    numFactura = StringField("", [validators.required()])
    orden = StringField("", [validators.required()])
    dep_soli = QuerySelectField("", query_factory = departamentos, get_pk=get_pk, allow_blank=True)
    nReq = StringField("", [validators.required()])
    oSoli = StringField("", [validators.required()])
    tCompra = StringField("", [validators.required()])
    obser = TextField("",[validators.required()])
    total = DecimalField('',  places=4, rounding=None)


class form_consul_entrada(Form):
    nOrden = StringField("",[validators.DataRequired(message = 'Debe proporcional el número de orden!.')])


class formbuscasalida(Form):
    order_id = StringField('',
        [validators.Required(message = 'Debe proporcional el número de entrada u orden!.'),
        validators.length(max = 12, message='El campo debe contener 12 caracteres como máximo')
        ])
    
    actividad = StringField('',
        [validators.Required(message = '¡Debe capturar la actividad para esta salida!')
        ])