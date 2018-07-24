import pprint
from flask import json, jsonify
from flaskie.api.v1.models import (
    MainModel,
    User,
    Requests
)
from datetime import datetime
from flaskie import v2_db

class DBCollector(MainModel):
    """This is the base model"""
    __table__ = ""
    
    @classmethod
    def deserialize(cls, dictionary):
        """Creates a model object"""
        return json.loads(json.dumps(dictionary, indent=4, sort_keys=True, default=str))

    @classmethod
    def get_all(cls):
        """Get all the items in the database"""
        v2_db.cursor.execute("SELECT * FROM {}".format(cls.__table__))
        items = v2_db.cursor.fetchall()
        return [cls.deserialize(item) for item in items]

    @classmethod
    def get_by_field(cls, field, value):
        """Get an item from the database by its key or field"""
        if cls.get_all() is None:
            return {}
        for item in cls.get_all():
            if item[field] == value:
                return item

    @classmethod
    def get_item_by_id(cls, _id):
        """Retrieves an item by the id provided"""
        v2_db.cursor.execute("SELECT * FROM {} WHERE id = %s".format(cls.__table__), (_id,))
        item = v2_db.cursor.fetchone()
        if item is None:
            return None
        return cls.deserialize(item)
    
    @classmethod
    def rollback(cls):
        """Deletes all the data from the tables"""
        v2_db.cursor.execute("DELETE FROM {}".format(cls.__table__))
        v2_db.connection.commit()

    def insert(self):
        """Inserts a new item in the database"""
        result = v2_db.cursor.fetchone()
        if result is not None:
            self.id = result['id']
        v2_db.connection.commit()

    def delete(self):
        """deletes an item from the database"""
        v2_db.cursor.execute("SELECT * FROM {} WHERE id = %s".format(self.__table__), (self.id))
        v2_db.connection.commit()

class User(User, DBCollector):
    __table__ = "users"

    def toJSON(self, dictionary):
        user = User()
        user.id = dictionary['id']
        user.name = dictionary['name']
        user.username = dictionary['username']
        user.email = dictionary['email']
        user.password_hash = dictionary['password_hash']
        user.registered_on = dictionary['registered_on']
        user.admin = dictionary['admin']

        return user

    @classmethod
    def migrate(cls):
        v2_db.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                name VARCHAR,
                username VARCHAR,
                email VARCHAR,
                password_hash VARCHAR,
                registered_on timestamp,
                admin BOOL
            )
            """
        )
        v2_db.connection.commit()

    def insert(self):
        """save to the database"""
        v2_db.cursor.execute(
            "INSERT INTO users(name, username, email,"
            "password_hash, registered_on, admin) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id", (
                self.name,
                self.username,
                self.email,
                self.password_hash,
                self.registered_on,
                self.admin
            )
        )
        super().insert()

    @classmethod
    def is_admin(cls):
        """
        To check if the user is an administrator
        :return:
        """
        return True

class Requests(Requests, DBCollector):
    __table__ = "requests"

    def toJSON(self, dictionary):
        requests = Requests()
        requests.created_by = dictionary['created_by']
        requests.id = dictionary['id']
        requests.requestname = dictionary['requestname']
        requests.description = dictionary['description']
        requests.date_created = dictionary['date_created']
        requests.date_modified = dictionary['date_modified']
        requests.status = dictionary['status']

        return requests
    
    @classmethod
    def migrate(cls):
        v2_db.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS requests(
                created_by INTEGER,
                id serial PRIMARY KEY,
                requestname VARCHAR,
                description VARCHAR,
                date_created timestamp,
                date_modified timestamp,
                status VARCHAR,
                FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        v2_db.connection.commit()

    def insert(self):
        """save to the database"""
        v2_db.cursor.execute(
            "INSERT INTO requests(created_by, requestname, description,"
            "date_created, date_modified, status) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id", (
                self.created_by,
                self.requestname,
                self.description,
                self.date_created,
                self.date_modified,
                self.status
            )
        )
        super().insert()

class BlackList(DBCollector):
    __table__ = "blacklist"

    def __init__(self, jti, blacklisted_on=datetime.now()):
        self.jti = jti
        self.blacklisted_on = blacklisted_on

    def toJSON(self, dictionary):
        blacklist = BlackList()
        blacklist.id = dictionary['id']
        blacklist.jti = dictionary['jti']
        blacklist.blacklisted_on = dictionary['blacklisted_on']
        
        return blacklist

    @classmethod
    def migrate(cls):
        v2_db.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS blacklist(
                id serial PRIMARY KEY,
                jti VARCHAR,
                blacklisted_on timestamp
            )
            """
        )
        v2_db.connection.commit()

    def insert(self):
        """save to the database"""
        v2_db.cursor.execute(
            "INSERT INTO blacklist(jti, blacklisted_on) VALUES(%s, %s) RETURNING id", (
                self.jti,
                self.blacklisted_on
            )
        )
        v2_db.connection.commit()