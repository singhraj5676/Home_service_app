from consts import const


DATABASE_CONFIG = {
    "host": const.RDS_HOST,
    "username": const.RDS_USERNAME,
    "password": const.RDS_PASSWORD,
    "port": const.RDS_PORT,
    "database": const.RDS_DATABASE
}

SECRET_KEY = const.SECRET_KEY
print("secret", SECRET_KEY)
ALGORITHM = const.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = const.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = const.REFRESH_TOKEN_EXPIRE_DAYS
