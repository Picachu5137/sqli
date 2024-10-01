from flask import Flask

from .config import SECRET_KEY

app = Flask(__name__, template_folder='template')
app.secret_key = SECRET_KEY

from . import routes
