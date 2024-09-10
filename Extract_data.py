import requests
import pandas as pd


Api_url = 'https://realty-in-us.p.rapidapi.com/properties/v3/list'
Api_header = {
    'Content-Type': 'application/json',
    'x-rapidapi-host' : 'realty-in-us.p.rapidapi.com',
    'x-rapidapi-key': 'aab8d83cbbmsh4ccd2b22c435304p101a71jsnc073ec211438'
}

Payload = {
    "limit":200,
    "offset":0,
    "postal_code":"90004",
    "status":["for_sale","ready_to_build"],
    "sort":{"direction":"desc","field":"list_date"}
}




def extract_data(api_url, headers, payload):
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    json_data = response.json()
    return json_data


def extract_required_data(data):

    results = data.get('data', {}).get('home_search', {}).get('results', [])
    extracted_data = []

    for i in results:
        location = i.get('location',{})
        address = location.get('address',{})
        description = i.get('description',{})

        estimate_info = i.get('estimate', {})
        estimate_value = estimate_info.get('estimate') if isinstance(estimate_info, dict) else None


        extracted_data.append({
            'property_id' : i.get('property_id'),
            'list_price': i.get('list_price'),
            'last_sold_price': i.get('last_sold_price'),
            'estimate': estimate_value,
            'list_date': i.get('list_date'),
            'status': i.get('status'),
            'city': address.get('city'),
            'state': address.get('state'),
            'postal_code': address.get('postal_code'),
            'type': description.get('type'),
            'lot_sqft': description.get('lot_sqft')
        })


    df = pd.DataFrame(extracted_data)


    df.drop_duplicates(inplace=True) 
    df.fillna({'estimate': 0, 'list_price': 0, 'lot_sqft': 0, 'last_sold_price': 0}, inplace=True) 
    df['list_price'] = pd.to_numeric(df['list_price'], errors='coerce')  
    df['estimate'] = pd.to_numeric(df['estimate'], errors='coerce')  
    df['list_date'] = pd.to_datetime(df['list_date'], errors='coerce')
    df['last_sold_price'] = pd.to_numeric(df['last_sold_price'], errors='coerce')
    
    return df


data = extract_data(Api_url,Api_header,Payload)
df = extract_required_data(data)
print(df.head())
df.to_csv('real_estate_data.csv',index = False)