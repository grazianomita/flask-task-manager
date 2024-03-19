from dotenv import load_dotenv

load_dotenv()

from app import create_app
from os import getenv
from config import get_config


app = create_app(get_config())

if __name__ == '__main__':
    app.logger.info('running app')
    app.run(port=getenv("FLASK_PORT"))
