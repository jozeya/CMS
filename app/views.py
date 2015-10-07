from flask import render_template, flash, redirect, session, url_for, request
from app import app, db, mail
from .forms import RecoverPassForm, CreateUserForm, ResetPasswordSubmit
from .models import User
from flask.ext.security.utils import encrypt_password, verify_password
from flask_mail import Mail, Message
from werkzeug import check_password_hash, generate_password_hash

@app.route('/')
@app.route('/signin')
def signin():
	return	render_template("signin.html")

@app.route('/index')
def index():
	user = {'nickname':'Miguel'}
	return render_template("index.html",user=user)

@app.route('/recover_pass', methods=('GET','POST'))
def recover_pass():
	form = RecoverPassForm()

	if form.validate_on_submit():
		email = form.email.data
		user = User.query.filter_by(email=email).first()

		if user:
			token = user.get_token()
			print token
			url = 'http://192.168.1.41:8080/change_pass?token=' + token
			send_mail(email,url)
			 
			return render_template("confirm.html",email=email)


	return render_template("recover_pass.html", form=form)

@app.route('/change_pass', methods=['GET','POST'])
def change_pass():
	token = request.args.get('token',None)
	verified_result = User.verify_token(token)
	if token and verified_result:
		print verified_result
		password_submit_form = ResetPasswordSubmit(request.form)

		if password_submit_form.validate_on_submit():
			verified_result.password = generate_password_hash(password_submit_form.password.data)
			db.session.commit()
			flash("password updated successfully")
			return redirect('users')
		return render_template("change_pass.html",form=password_submit_form)
		

@app.route('/users')
def users():
	user = User.query.filter().all()
	return render_template("users.html",user=user)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
	form = CreateUserForm()

	if form.validate_on_submit():
		user = User(id=form.id.data, nickname = form.nickname.data, 
			email=form.email.data, password=generate_password_hash(form.password.data))

		db.session.add(user)
		db.session.commit()
		return redirect('/users')
	return render_template("create_user.html",form=form)

@app.route('/send_mail')
def send_mail(email,url):
	msg = Message("Recupera tu Contrasenia", sender="pruebas.cms@asacoop.com",
	 recipients=[email])
	msg.body = "Este mensaje te llego porque solicitaste recuperar tu contrasenia, utiliza esta direccion de correo " + url
	mail.send(msg)
	return redirect('/index')
