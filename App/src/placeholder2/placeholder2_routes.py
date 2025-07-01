from flask import Blueprint
from flask_restx import Api, Resource

placeholder2 = Blueprint('placeholder2', __name__, url_prefix='/placeholder2')
api = Api(placeholder2)
placeholder2_ns = api.namespace('placeholder2', description='Placeholder 2')
api.add_namespace(placeholder2_ns)

@placeholder2_ns.route('/')
class Placeholder2Root(Resource):
    def get(self):
        return {"placeholder2": "placeholder2"}