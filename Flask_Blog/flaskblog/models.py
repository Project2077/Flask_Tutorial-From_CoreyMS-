from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flaskblog import db, login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    # password will be hash,It's going to make this 60 characters
    posts = db.relationship('Post', backref='author', lazy=True)
    # the backref is similar to adding another column to the post model 
    # what the backref allows us to do is when we have a post we can simply this author attribute to get the user who created
    # 简单说：我们在Post(底下的)中加了一个属性叫author,这个author返回的是当前User对象
    # the lazy arg just defines when SQL alchemy loads the data from the database 
    # so true means that SQL alchemy will load the data the data as necessary in one go
    # lazy参数选择什么值，决定了 SQLAlchemy 什么时候从数据库中加载数据。 true 就是使用'select'方法
    # lazy参数用于指定sqlalchemy数据库什么时候加载数据。lazy=true代表延时加载，lazy=false代表不延时，不延时代表查询出对象A的时候，会把B对象也查询出来放到A对象的引用中，A对象中的B对象是有值的。延时则查询A对象时，不会把B对象也查询出来，只会在用到A对象中B对象时才会去查询。
    # 视频讲的类似上边这句

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}).encode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(
                token,
                max_age=1800
            )['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        # this does this specifically is how our object is printed whenever we print it out.
        # 把object打印成String给我们看
        return f"User('{self.username}, {self.email}, {self.image_file})"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # 需要引入 datetime
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}, {self.date_posted})"