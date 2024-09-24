import psycopg2
from models.user_models import Base
from config import DATABASE_CONFIG
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class POSTGRES_API:
    def __init__(self, host, username, password, port, database):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.database = database
        
        # Correct connection string format for SQLAlchemy
        self.engine = create_engine(
            f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
        )
        print(f"Database configuration: {self.host}, {self.username}, {self.password}, {self.port}, {self.database}")
        
        self.Session = sessionmaker(bind=self.engine)
        self.conn = None

    def connect(self):
        print("Connecting")
        # Correct parameters for psycopg2.connect
        self.conn = psycopg2.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            port=self.port,
            dbname=self.database
        )
        print("Connected")

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    # def create_tables(self):
    #     print('Creating')
    #     Base.metadata.create_all(self.engine)
    def create_tables(self):
        try:
            print('Attempting to create tables...')
            Base.metadata.create_all(self.engine)
            print('Tables created successfully.')
        except Exception as e:
            print(f'Error creating tables: {e}')


    def execute_query(self, query, params=None):
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            self.conn.commit()

    def fetch_query(self, query, params=None):
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def get_session(self):
        return self.Session()


def get_db():
    print('Getting DB')
    db = POSTGRES_API(**DATABASE_CONFIG)
    try:
        session = db.get_session()
        yield session
    finally:
        db.close()
    
    