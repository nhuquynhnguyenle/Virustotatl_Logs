import requests
import json
import os

class virustotal:
    
    #Method getting value API_KEY in configure.json file
    def getJsonKey(self):
        file_path = 'configure.json'
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        api_key = json_data["API_KEY"]
        return api_key

    #Method getting id of url which has been checked by virustotal  
    def get_uid(self,url,api_key):
        params = {
        "apikey": api_key,
        "resource": url
        }    
        response = requests.get("https://www.virustotal.com/vtapi/v2/url/report", params=params)
        data = response.json()    
        if response.status_code == 200:
            url_id = data.get("scan_id")
            index = url_id.find('-')
            url_id = url_id[:index]
            return url_id

    #Method getting community score of the checked url from virustotal 
    def get_score (self,url_id,api_key):
        url_virustt = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        headers = {'x-apikey': api_key}
        response = requests.get(url_virustt, headers=headers)
        data = response.json()
        if response.status_code == 200:
            community_score = data['data']['attributes']['last_analysis_stats']['malicious']
            return community_score
        else:
            return None

    #Method scanning the url that has not been checked by Virus total
    def scan_url(self,url, api_key):
        scan_url = 'https://www.virustotal.com/vtapi/v2/url/scan'
        params = {'apikey': api_key, 'url': url}

        response = requests.post(scan_url, data=params)
        json_response = response.json()

        if response.status_code == 200:
            if json_response['response_code'] == 1:
                scan_id = json_response['scan_id']
            #Remove timestamps appended after url id
                scan_id = scan_id.split('-')[0]
                return scan_id
    
    

