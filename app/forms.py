from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
#from wtforms import validators

class LoginForm(Form):
	openid = StringField('openid', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class RecoverPassForm(Form):
	email = StringField('r_email', validators=[DataRequired()])

class ChangePassForm(Form):
	newpass1 = StringField('rpass1', validators=[DataRequired()])
	newpass2 = StringField('rpass2', validators=[DataRequired()])

class CreateUserForm(Form):
	id = StringField('id', validators=[DataRequired()])
	nickname = StringField('nickname', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('pass', validators=[DataRequired()])

"""class ExistingUser(object):
	def __init__ (self, message="Email doesn't exists"):
		self.message = message

	def __call__ (self, form, field):
		if not Local_User.query.filter_by(email=field.data).first():
			raise ValidationError(self.message)

	reset_rules = [validators.Required(), validators.Email()] #, ExistingUser(message='Email address is not available')]

class ResetPassword(Form):
	email = StringField('Email', validators=reset_rules)

class ResetPasswordSubmit(Form):
	password = PasswordField('Password', validators=custom_validators['edit_password'], )
	confirm = PasswordField('Confirm Password')"""


