from flaskie.api.v2.models import User, BlackList

class Migration:
    @staticmethod
    def refresh():
        Migration.tear_down()
        Migration.set_up()

    @staticmethod
    def set_up():
        """Creates the tables"""
        User.migrate()
        BlackList.migrate()

    @staticmethod
    def tear_down():
        """Deletes data from the the tables"""
        User.rollback()
        BlackList.rollback()