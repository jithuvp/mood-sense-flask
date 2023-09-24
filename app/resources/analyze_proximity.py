from geopy import distance

import pandas as pd
import json

def check_proximity(payload, current_location):
    '''
    Calculates the distance b/w coordinates of current location and ALL
    locations where Mood state/characteristic == happy
    '''
    data = pd.json_normalize(payload)
    print(data)

    # Exclude states other than 'happy'
    data = data[data['state'] == 'happy']

    #combine two columns to list
    data['coords'] = list(zip(data['location.lat'], data['location.long']))

    #calculate distance
    data['distance_to_in_kms'] = data['coords'].apply(lambda x: distance.distance(current_location, x).km)
    data = data.rename(columns={'location.type': 'type'})

    #select columns and convert to json
    processed_data = data[['type', 'distance_to_in_kms']].to_json(orient='records')

    return json.loads(processed_data)
