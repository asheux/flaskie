from flaskie import create_app
from flaskie import settings
from migrate import Migration

migrate = Migration()
app = create_app(settings.DEVELOPMENT)

if __name__ == "__main__":
    # migrate.tear_down()
    migrate.set_up()
    app.run(debug=settings.FLASK_DEBUG)