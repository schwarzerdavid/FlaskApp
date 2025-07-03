from flask import Blueprint
from flask_restx import Api, Resource

placeholder1 = Blueprint('placeholder1', __name__, url_prefix='/placeholder1')
api = Api(placeholder1)
placeholder1_ns = api.namespace('placeholder1', description='Placeholder 1')

@placeholder1_ns.route('/')
class Placeholder1Root(Resource):
    def get(self):
        "placeholder 1 documentation"
        return {"placeholder1": "placeholder1"}, 200