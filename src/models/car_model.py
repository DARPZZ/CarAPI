from pydantic import BaseModel
class Car(BaseModel):
    regNr: str
    status: str
    rentedcar: bool
    leasingPeriode: str
    car_name_type: str
    car_model_type: str
    modelÅr: int
    motor_størrelse: float
    motor_hestekræfter: float
    motorKmPerLiter: float