from App.src.entities.operation_room import OperationRoom
from App.src.enums.equipment_enum import EquipmentEnum

HOSPITAL_ORS = (
    OperationRoom(id = 1, equipment = [EquipmentEnum.MRI, EquipmentEnum.ECG]),
    OperationRoom(id = 2, equipment = [EquipmentEnum.MRI, EquipmentEnum.ECG]),
    OperationRoom(id = 3, equipment=[EquipmentEnum.MRI, EquipmentEnum.CT, EquipmentEnum.ECG]),
    OperationRoom(id = 4, equipment = [EquipmentEnum.MRI, EquipmentEnum.CT]),
    OperationRoom(id = 5, equipment = [EquipmentEnum.MRI, EquipmentEnum.CT]),
)