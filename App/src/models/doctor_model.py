from flask_restx import fields, Namespace
from App.src.enums.doctor_types import DoctorTypes

def get_doctor_model(ns: Namespace):
    return ns.model('DoctorRequest', {
    'doctor_type': fields.String(
        required=True,
        description='Type of doctor',
        enum=[dt.value for dt in DoctorTypes]
    )
})