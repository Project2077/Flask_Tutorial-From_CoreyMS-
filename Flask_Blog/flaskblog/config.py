import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # with sqlite we can specify a relative path with three ford slashes in the URI 
    # these three slashes are a relative path from the current file
    # 使用 sqlite，我们可以在 URI 中指定带有三个福特斜杠的相对路径
    MAIL_SERVER = 'smtp.googlemail.com' 
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')