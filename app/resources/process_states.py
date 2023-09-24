import pandas as pd
import json

def get_freq_dist(payload):
    data = pd.json_normalize(payload)
    data = data['state'].value_counts(normalize=True)*100
    processed_data = pd.DataFrame({
    	'state': data.index, 
    	'proportion_percent': data.values}) \
    .to_json(orient='records')
    
    return json.loads(processed_data)
