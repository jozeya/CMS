from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid, mail
from .forms import LoginForm, RecoverPassForm, ChangePassForm, CreateUserForm
from .models import User
from flask.ext.security.utils import encrypt_password, verify_password
from flask_mail import Mail, Message

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/practice')
@login_required
def practice():
	#user = {'nickname':'Miguel'}
	user = g.user
	posts = [
				{'author':{'nickname':'John'}, 'body':'Beautiful day in Portland'},
				{'author':{'nickname':'Susan'}, 'body':'The Avengers movie was so cool'}
		    ]
	return render_template("practice.html", title='Home', user=user, posts=posts)

@app.route('/index')
def index():
	user = {'nickname':'Miguel'}
	return render_template("index.html",user=user)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
	return render_template('login.html', title='Sign In', form=form, providers=app.config['OPENID_PROVIDERS'])
		#flash('Login Requested form OpenID="%s", remember_me=%s' % (form.openid.data, str(form.remember_me.data)))
		#return	redirect('/practice')
	#return render_template("login.html", title='Sign In', form=form, providers=app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash('invalid login. Please try again.')
		return redirect(url_for('login'))

	user = User.query.filter_by(email=resp.email).first()

	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]

		user = User(nickname=nickname, email=resp.email)

		db.session.add(user)
		db.session.commit()

	remember_me = False

	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)

	login_user(user, remember = remember_me)
	return redirect(request.args.get('next') or url_for('index'))

@app.before_request
def before_request():
	g.user = current_user

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

"""@mod.route('/reset-password', methods=('GET', 'POST',))
def forgot_password():
	token = request.args.get('token', None)
	form = ResetPassword(request.form)

	if form.validate_on_submit():
		email = form.email.data
		user = Local_User.query.filter_by(email=email).first()

		if user:
			token = user.get_token()
			print token

	return render_template('reset.html', form=form)"""

@app.route('/recover_pass')
def recover_pass():
	form = RecoverPassForm()
	return render_template("recover_pass.html", form=form)

@app.route('/change_pass')
def change_pass():
	form = ChangePassForm()
	return render_template("change_pass.html", form=form)

@app.route('/users')
def users():
	user = User.query.filter().all()
	return render_template("users.html",user=user)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
	form = CreateUserForm()

	if form.validate_on_submit():
		user = User(id=form.id.data, nickname = form.nickname.data, 
			email=form.email.data, password=encrypt_password(form.password.data))

		db.session.add(user)
		db.session.commit()
		return redirect('/users')
	return render_template("create_user.html",form=form)

@app.route('/send_mail')
def send_mail():
	msg = Message("Hello Alferx - 3", sender="pruebas.cms@asacoop.com",
	 recipients=["alfredo.morote@ucsp.edu.pe"])
	msg.body = "Animalazo hace rato te estoy diciendo si sale subject"
	mail.send(msg)
	return redirect('/index')

#pythonhosted.org/Flask-Mail
