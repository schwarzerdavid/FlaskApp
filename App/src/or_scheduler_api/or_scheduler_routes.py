from flask import Blueprint, request
from flask_restx import Api, Resource

from App.src.entities.assign_respone import AssignResponse
from App.src.entities.or_request import ORRequest
from App.src.enums.doctor_types import DoctorTypes
from App.src.global_scheduler_manager import global_scheduler_manager
from App.src.models.doctor_model import get_doctor_model

or_scheduler_api = Blueprint('or_scheduler_api', __name__, url_prefix='/or_scheduler_api')
api = Api(or_scheduler_api)
or_scheduler_api_ns = api.namespace('', description='API for scheduling OR Rooms')
doctor_model = get_doctor_model(or_scheduler_api_ns)


@or_scheduler_api_ns.route('/request_time')
class RequestSpot(Resource):
    @or_scheduler_api_ns.expect(doctor_model)
    def post(self):
        """A Doctor requests the next available operation slot
        :returns: the operation room id + time, or place in queue"""
        data = request.json
        try:
            doctor_type = DoctorTypes(data['doctor_type'])
        except ValueError:
            return {"message": "Invalid doctor_type"}, 400

        or_request = ORRequest(doctor_type=doctor_type)

        response: AssignResponse = global_scheduler_manager.handle_or_request(or_request)
        return { "is_assigned": response.is_assigned,
                 "starting_day": response.room_slot.starting_day if response.room_slot else None,
                 "starting_hour": response.room_slot.starting_hour if response.room_slot else None,
                 "room_id": response.room_slot.room_id if response.room_slot else None,
                 "place_in_queue": response.place_on_queue
                 }