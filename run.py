from flaskie import create_app
from flaskie import settings

app = create_app(settings.DEVELOPMENT)

if __name__ == "__main__":
    app.run(debug=settings.FLASK_DEBUG)