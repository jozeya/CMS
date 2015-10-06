from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask import session, redirect, current_app
#from app import app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    #password = db.Column(db.String(200), index=True, unique=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

"""class Local_User(db.Model, UserMixin):
	__tablename__ = 'myusers'

	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	active = db.Column(db.Boolean())
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120))

	def get_token(self, expiration=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'user': self.id}).decode('utf-8')

	@staticmethod
	def verify_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return None

		id = data.get('user')
		if id:
			return Local_User.query.get(id)
		return None  """

"""security = Security()
user_datastore = SQLAlchemyUserDatastore(db,User,Post)
security.init_app(app,user_datastore)"""
