from flask import Flask

from App.src.placeholder1.placeholder1_routes import placeholder1
from App.src.placeholder2.placeholder2_routes import placeholder2

app = Flask(__name__)
app.register_blueprint(placeholder1)
app.register_blueprint(placeholder2)