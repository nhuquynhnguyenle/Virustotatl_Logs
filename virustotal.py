import requests
import json

URL = input("Enter Url: ")

#Method getting value API_KEY in configure.json file
def getJsonKey():
    file_path = 'configure.json'
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    api_key = json_data["API_KEY"]
    return api_key

#Method getting id of url which has been checked by virustotal  
def get_uid():
    api_key = getJsonKey()
    params = {
    "apikey": api_key,
    "resource": URL
    }
    response = requests.get("https://www.virustotal.com/vtapi/v2/url/report", params=params)
    data = response.json()    
    if response.status_code == 200:
        url_id = data.get("scan_id")
        index = url_id.find('-')
        url_id = url_id[:index]
        return url_id

#Method getting community score from virustotal 
def get_score ():
    api_key = getJsonKey()
    url_id = get_uid()
    url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    headers = {'x-apikey': api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        community_score = data['data']['attributes']['last_analysis_stats']['malicious']
        print(f"Community score: {community_score}")
    else:
        print("Can not access to VirusTotal API.")
