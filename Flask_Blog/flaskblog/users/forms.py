from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    # 继承了Flask的基础表单FlaskForm
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])   # 长，调以下像这样 vscode一个enter ok
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', 
                                     validators=[DataRequired(),EqualTo('password')] )   # EqualTo('password')也在valdators中！！！！！
    
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken.Please choose a different one.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken.Please choose a different one.')


class LogInForm(FlaskForm):
    # 复制的RegistrationForm后改的
    email = StringField('Email', 
                           validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])  
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:  # 如果用户要更新的username不是原username,检测是否有重复的，有就回复这个validationError
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken.Please choose a different one.')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken.Please choose a different one.')
            

class RequestResetForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    # grab from UpdateAccountForm  只需要一个邮箱和一个提交  邮箱自定义校验器

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', 
                                     validators=[DataRequired(),EqualTo('password')] )
    submit = SubmitField('Reset Password')
    # grab from RegistrationForm  