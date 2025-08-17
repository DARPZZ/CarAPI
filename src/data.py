import os
import requests
from src.models.car_model import Car
from dotenv import load_dotenv
load_dotenv()
async def get_data(nummerplade):
    START_URL = os.getenv("data_url")
    url = f"{START_URL}{nummerplade}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            car_info = response.json()
            return car_info
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

async def exstract_data(nummerplade):
    car_data = await get_data(nummerplade)
    #region basic car data
    basic_car_data = car_data['basic']
    regnummer = basic_car_data.get('regNr')
    status = basic_car_data.get('status')
    rented_car = basic_car_data.get('bilLeaset')
    leasingPeriode = basic_car_data.get('leasingPeriode')
    maerkeTypeNavn = basic_car_data.get('maerkeTypeNavn')
    modelTypeNavn = basic_car_data.get('modelTypeNavn')
    modelÅr = basic_car_data.get('modelAar')
    motorStoerrelse = basic_car_data.get('motorStoerrelse')
    motor_hestekræfter = basic_car_data.get('motorHestekraefter')
    motorKmPerLiter =basic_car_data.get('motorKmPerLiter')
    #endregion
    return Car(
       regNr=regnummer,
       status=status,
       rentedcar=rented_car,
       leasingPeriode=leasingPeriode,
       car_name_type= maerkeTypeNavn,
       car_model_type=modelTypeNavn,
       modelÅr=modelÅr,
       motor_størrelse=motorStoerrelse,
       motor_hestekræfter=motor_hestekræfter,
       motorKmPerLiter=motorKmPerLiter       
    )