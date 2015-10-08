from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for
)
from werkzeug import check_password_hash, generate_password_hash

from app import db
from app.authentication.forms import LoginForm
from app.authentication.models import User


mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Welcome %s' % user.name)
            return redirect(url_for('auth.home'))

        flash('Wrong email or password', 'error-message')

    return render_template("authentication/signin.html", form=form)

@mod_auth.route('/recover_pass', methods=('GET','POST'))
def recover_pass():
    form = RecoverPassForm()

    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if user:
            token = user.get_token()
            print token
            url = 'http://0.0.0.0:8080/change_pass?token=' + token
            send_mail(email,url)
             
            return render_template("confirm.html",email=email)


    return render_template("recover_pass.html", form=form)
