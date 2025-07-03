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
class RequestTime(Resource):
    @or_scheduler_api_ns.expect(doctor_model)
    def post(self):
        """
        Request the next available operating room slot.

        Accepts a doctor type and returns either:
        - a scheduled operation room slot with room ID, day, and hour
        - or the doctor's place in the pending queue if no room is available

        **Request Body:**
        - doctor_type (str): One of the supported doctor types, e.g., "HEART_SURGEON", "BRAIN_SURGEON"

        **Responses:**
        - 200 OK: JSON object with assignment result and slot details or queue position

                  JSON structure:
                  { "is_assigned": True for time assigned, False for getting request to queue,
                    "starting_day": if assigned -> days from tomorrow (0 - tomorrow, 1 - the after, etc.
                    "starting_hour": if assigned -> hour in the day
                    "room_id": if assigned -> operation room id
                    "place_in_queue": if not assigned -> place in queue
                 }
        - 400 Bad Request: Invalid doctor_type provided
        """
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

@or_scheduler_api_ns.route('/day_passed')
class RequestSpot(Resource):
    def post(self):
        """
        Advance the scheduler to the next day.

        Simulates the passing of a hospital day:
        - Clears out passed operation slots
        - Frees up time in the operation room schedule
        - Schedule Requests from queue if exist

        **Responses:**
        - 200 OK: The day was successfully advanced
        """
        global_scheduler_manager.day_pass()
        return {}, 200