from sqlalchemy import create_engine
import psycopg2

config = {
    'user': 'mainportfolio_eyl8_user',
    'password': '25ozI3Z5tgT8my1vf6sfQbFZ7qTvzLY0',
    'host': 'dpg-cqg44qd6l47c73botspg-a.oregon-postgres.render.com',
    'database': 'mainportfolio_eyl8'
}

# Connect to PostgreSQL using psycopg2
connection = psycopg2.connect(
    user=config['user'],
    password=config['password'],
    host=config['host'],
    database=config['database']
)

SECRET_KEY = "THTD673&?/YHG/@H393_YEU"
ADMIN_EMAIL = "admin@personal.com"
USER_PROFILE_PATH="myport/static/assets/images/profile/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root@127.0.0.1/MainPortfolio"

# SQLAlchemy database URI for PostgreSQL
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://mainportfolio_eyl8_user:25ozI3Z5tgT8my1vf6sfQbFZ7qTvzLY0@dpg-cqg44qd6l47c73botspg-a.oregon-postgres.render.com/mainportfolio_eyl8"
# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)


MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'carryoby@gmail.com'
MAIL_PASSWORD = 'pzvw jfdf swwa lmcw'
MAIL_USE_SSL = True