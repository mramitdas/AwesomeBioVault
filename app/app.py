from flask import Flask
from .api.V1.endpoints.user import user

app = Flask(__name__)
app.register_blueprint(user, url_prefix='/')
