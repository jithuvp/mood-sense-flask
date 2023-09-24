import random

#pre-selected location characteristics
TYPES = ['Home', 'Work', 'Supermarket', 'Beach', 'Shopping Mall']

def location_type_selector(lat, long):
    '''
    Assign a random type to location. In reality, this must be replaced
    by a 3rd party lib for obtaining location characteristics based on the
    GPS coordinates
    '''

    return random.choice(TYPES)


