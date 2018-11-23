from wtforms import Form
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from wtforms import PasswordField
from wtforms import HiddenField
from wtforms import validators
from models import User


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
    
        