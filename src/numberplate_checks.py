
def check_danish_numberplate(number_plate_stripped):
    if(len(number_plate_stripped)< 7):
        return False
    if (number_plate_stripped[0:2].isalpha() and number_plate_stripped[3:7].isdigit()):
        return True