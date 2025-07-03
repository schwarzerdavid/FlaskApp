from collections import deque
from typing import Optional

from App.src.consts.hospital_ors import HOSPITAL_ORS
from App.src.consts.scheduler_consts import SCHEDULER_PERIOD_IN_DAYS, TWO_HOURS, THREE_HOURS, NO_ROOM_ASSIGNED, \
    OR_WORKING_HOURS_A_DAY, EMPTY_SLOT_REQUEST_ID
from App.src.entities.Hospital import Hospital
from App.src.entities.assign_respone import AssignResponse
from App.src.entities.operation_room import OperationRoom
from App.src.entities.or_request import ORRequest
from App.src.entities.room_slot import RoomSlot
from App.src.enums.doctor_types import DoctorTypes
from App.src.enums.equipment_enum import EquipmentEnum


class ORSchedulerManager:
    def __init__(self):
        self._hospital: Hospital = self._init_hospital_rooms()
        self._pending_requests = deque()
        self._request_id_counter = 0


    def _init_hospital_rooms(self) -> Hospital:
        return Hospital(operation_rooms=HOSPITAL_ORS)

    def handle_or_request(self, or_request: ORRequest) -> AssignResponse:
        self._request_id_counter += 1
        or_request.request_id = self._request_id_counter
        room_slot = self._get_and_assign_next_available_slot(or_request)
        if room_slot.is_empty():
            self._pending_requests.append(or_request)
            return AssignResponse(is_assigned=False, place_on_queue=len(self._pending_requests))
        else:
            return AssignResponse(is_assigned=True, room_slot=room_slot)

    def day_pass(self):
        self._move_time_table_one_day()
        for i in range(len(self._pending_requests)):
            req = self._pending_requests.popleft()
            response = self.handle_or_request(req)
            if response.is_assigned == False:
                self._pending_requests.append(req)


    def _get_and_assign_next_available_slot(self, or_request: ORRequest) -> RoomSlot:
        # this algorythm assign the room based only on the closest time available
        # if we want to prioritize by time assigned, we can check first for the time assigned in the RoomSlot and only if equal or lower
        # to current, take it is as the current
        current_room_slot = RoomSlot()
        for or_room in self._hospital.operation_rooms:
            time_needed = self._get_room_needed_time(or_request, or_room)
            if time_needed:
                room_slot = self._get_closest_slot_available(or_room, time_needed)
                if room_slot.is_sooner_then(current_room_slot):
                    current_room_slot = room_slot
                    current_room_slot.time_assigned = time_needed
        if current_room_slot.room_id != NO_ROOM_ASSIGNED:
            self._assign_time_slot(or_request, current_room_slot)
        return current_room_slot


    def _get_room_needed_time(self, or_request:ORRequest, or_room: OperationRoom) ->Optional[int]:
        if or_request.doctor_type == DoctorTypes.HEART_SURGEON and EquipmentEnum.ECG in or_room.equipment:
            return THREE_HOURS
        if or_request.doctor_type == DoctorTypes.BRAIN_SURGEON and EquipmentEnum.MRI in or_room.equipment and EquipmentEnum.CT in or_room.equipment:
            return TWO_HOURS
        if or_request.doctor_type == DoctorTypes.BRAIN_SURGEON and EquipmentEnum.MRI:
            return THREE_HOURS
        return None

    def _get_closest_slot_available(self, or_room: OperationRoom, time_needed: int) -> RoomSlot:
        for day in range(SCHEDULER_PERIOD_IN_DAYS):
            for hour in range(OR_WORKING_HOURS_A_DAY):
                if len(or_room.scheduler.time_table[day][hour:]) < time_needed:
                    continue
                if all(request_id == EMPTY_SLOT_REQUEST_ID for request_id in or_room.scheduler.time_table[day][hour: hour + time_needed]):
                    return RoomSlot(room_id=or_room.id,
                                    starting_hour=hour,
                                    starting_day=day)
        return RoomSlot()

    def _assign_time_slot(self, or_request: ORRequest, room_slot: RoomSlot):
        for hour in range(room_slot.starting_hour, room_slot.starting_hour + room_slot.time_assigned):
            operation_room: OperationRoom = self._get_room_by_id(room_slot.room_id)
            operation_room.scheduler.time_table[room_slot.starting_day][hour] = or_request.request_id

    def _get_room_by_id(self, room_id):
        for or_room in self._hospital.operation_rooms:
            if or_room.id == room_id:
                return or_room

    def _move_time_table_one_day(self):
        for or_room in self._hospital.operation_rooms:
            for day in range(SCHEDULER_PERIOD_IN_DAYS - 1):
                or_room.scheduler.time_table[day] = or_room.scheduler.time_table[day + 1]
            or_room.scheduler.time_table[SCHEDULER_PERIOD_IN_DAYS - 1] = [0] * OR_WORKING_HOURS_A_DAY

