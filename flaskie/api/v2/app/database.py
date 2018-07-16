import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    connection = None
    cursor = None
    app = None

    def init_app(self, app):
        self.app = app
        self.connection = psycopg2.connect(
            dbname=app.config['DATABASE_NAME'],
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASSWORD'],
            host=app.config['DATABASE_HOST']
        )
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)