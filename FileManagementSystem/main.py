from app import create_app
from config import CONFIG

config = CONFIG()
app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True,
        host=config["HOST"],
        port=config["PORT"],
    )
