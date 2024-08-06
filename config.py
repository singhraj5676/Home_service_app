from consts import const


DATABASE_CONFIG = {
    "host": const.RDS_HOST,
    "username": const.RDS_USERNAME,
    "password": const.RDS_PASSWORD,
    "port": const.RDS_PORT,
    "database": const.RDS_DATABASE
}
print('data',DATABASE_CONFIG)
