$('#loginForm').bootstrapValidator({
  message: 'Este valor no es valido',
	feedbackIcons: {
	  valid: 'glyphicon glyphicon-ok',
	  invalid: 'glyphicon glyphicon-remove',
	  validating: 'glyphicon glyphicon-refresh'
	},
	fields: {
	  nnombre: {
		validators: {
		  notEmpty: { message: 'El nombre de usuario es requerido'},
          stringLength: {
            min: 4,
            max: 30,
            message: 'El nombre de usuario debe tener entre 6 y 30 caracteres de logitud'
          },
          regexp: { 
            regexp: /^[a-zA-Z0-9_]+$/,
            message: 'The username can only consist of alphabetical, number and underscore'
          }
        }
      },
	npassword: {
	  validators: {
		notEmpty: { message: 'La contraseña es requerida'}
	  }
   }
 }
});