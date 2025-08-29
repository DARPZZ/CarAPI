import os
import requests
from src.models.car_model import Car
from dotenv import load_dotenv
load_dotenv()
async def get_data(nummerplade):
    START_URL = os.getenv("data_url")
    url = f"https://www.tjekbil.dk/api/v3/dmr/regnr/{nummerplade}"
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

    
def koeretoejUdstyr(basic_car_data):
    udstyr_liste = []
    koeretoejUdstyrSamling = basic_car_data.get('koeretoejUdstyrSamling')
    for udstyr in koeretoejUdstyrSamling:
        udstyr_liste.append(udstyr)
    return udstyr_liste
async def exstract_data(nummerplade):
    car_data = await get_data(nummerplade)  
    if(car_data is None):
        return None
    #region basic car data
    basic_car_data = car_data['basic']
    regnummer = basic_car_data.get('regNr')
    status = basic_car_data.get('status')
    rented_car = basic_car_data.get('bilLeaset')
    leasingPeriode = basic_car_data.get('leasingPeriode') or "Ingen leasing periode"
    maerkeTypeNavn = basic_car_data.get('maerkeTypeNavn')
    modelTypeNavn = basic_car_data.get('modelTypeNavn')
    modelÅr = basic_car_data.get('modelAar')
    motorStoerrelse = basic_car_data.get('motorStoerrelse')
    motor_hestekræfter = basic_car_data.get('motorHestekraefter')
    motorKmPerLiter =basic_car_data.get('motorKmPerLiter')
    totalVaegt = basic_car_data.get('totalVaegt')
    drivkraftTypeNavn = basic_car_data.get('drivkraftTypeNavn')
    maksimumHastighed = basic_car_data.get('maksimumHastighed')
    motorCylinderAntal = basic_car_data.get('motorCylinderAntal')
    antalDoere = basic_car_data.get('antalDoere')
    #endregion
    #region extendedinfo
    extended_car_data = car_data['extended']
    insurance = extended_car_data['insurance']
    insurance_selskab  = insurance.get('selskab')
    insurance_historik = insurance.get('historik')
    historik_liste = []
    for historik in insurance_historik:
        selskab = historik.get('selskab')
        status = historik.get('status')
        oprettet = historik.get('oprettet')
        historik_liste.append({
            'selskab': selskab,
            'status': status,
            'oprettet': oprettet
        })
    
    #endregion
    #region køretøjudstyr
    udstyr_liste = koeretoejUdstyr(basic_car_data)
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
       motorKmPerLiter=motorKmPerLiter,
       totalVaegt=totalVaegt,
       drivkraftTypeNavn=drivkraftTypeNavn,
       udstyr_liste=udstyr_liste,
       maksimumHastighed=maksimumHastighed,
       motorCylinderAntal=motorCylinderAntal,
       antalDoere = antalDoere,
       insurance = historik_liste
       
    )