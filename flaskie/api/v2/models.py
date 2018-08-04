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
        """
        Get an item from the database by its key or field
        if cls.get_all() is None:
            return {}
        for item in cls.get_all():
            if item[field] == value:
                return item
        """
        v2_db.cursor.execute("SELECT * FROM {0} WHERE {1} = %s".format(cls.__table__, field), (value,))
        items = v2_db.cursor.fetchall()

        return [cls.deserialize(item) for item in items]
    
    @classmethod
    def get_one_by_field(cls, field, value):
        items = cls.get_by_field(field, value)
        if len(items) == 0:
            return None
        return items[0]

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

    def toJSON(self):
        user = {
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'email': self.registered_on,
            'admin': self.admin
        }

        return self.deserialize(user)

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

    def updateuser(self, _id):
        self.registered_on = datetime.now()
        v2_db.cursor.execute(
            "UPDATE users SET name = %s, username = %s, email = %s,"
            "password_hash = %s, admin = %s WHERE id = %s", (
                self.name,
                self.username,
                self.email,
                self.password_hash,
                self.admin,
                _id
            )
        )
        v2_db.connection.commit()

class Requests(Requests, DBCollector):
    __table__ = "requests"

    def toJSON(self):
        requests = {
            'requestname': self.requestname,
            'description': self.description,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'status': self.status,
        }

        return self.deserialize(requests)
    
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

    def updaterequest(self, _id):
        self.date_modified = datetime.now()
        v2_db.cursor.execute(
            "UPDATE requests SET requestname = %s, description = %s, "
            "status = %s, date_modified = now() WHERE id = %s", (
                self.requestname,
                self.description,
                self.status,
                _id
            )
        )
        v2_db.connection.commit()

class BlackList(DBCollector):
    __table__ = "blacklist"

    def __init__(self, jti, blacklisted_on=datetime.now()):
        self.jti = jti
        self.blacklisted_on = blacklisted_on

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