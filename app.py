from getpass import getpass
import sys
from flaskie.api.v1.auth.errors import check_valid_email
from flaskie.api.v2.models import User
from flaskie import create_app
from flaskie import settings, log
from migrate import Migration

migrate = Migration()
app = create_app(settings.DEVELOPMENT)

@app.cli.command()
def createsuperuser():
    with app.app_context():
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
            return
        if check_valid_email(email) is None:
            print('Not a valid email address, please try again')
            return
        else:
            user = User(name, username, email, password, admin=True)
            user.insert()
            print('Admin created successfully')


if __name__ == "__main__":
    # migrate.tear_down()
    migrate.set_up()
    app.run(debug=settings.FLASK_DEBUG)