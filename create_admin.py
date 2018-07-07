from flask_script import Manager
from flask import Flask
from getpass import getpass
import sys
from flaskie.database import db
from flaskie.api.v1.auth.errors import check_valid_email
from flaskie.api.v1.models import User
from flaskie.api.v1.auth.collections import store

def main():
    from run import app, log
    with app.app_context():
        create = input('Do you want to create superuser? (y/n): ')
        if create == 'n':
            return
        log.info('Creating superuser.....')
        counter = 0
        name = input('Enter name: ')
        username = input('Enter username: ')
        email = input('Enter email: ')
        password = getpass('Enter password: ')
        try:
            assert password == getpass('Confirm password: ')
        except AssertionError as e:
            print('The password did match, try again')
            sys.exit()
        if check_valid_email(email) is None:
            print('Not a valid email address, please try again')
            main()
        else:
            user = User(name, username, email, password, admin=True)
            admin_id = username + '00%d' % counter
            db[admin_id] = user.toJSON()
            print('Admin created successfully')
            print(db)

if __name__ == '__main__':
    main()