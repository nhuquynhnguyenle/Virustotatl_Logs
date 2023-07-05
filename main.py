import time
from log_management import log_management
import json
from virustotalDB import controlDB
from virustotal import virustotal

file_path = 'access.log'
management = log_management(file_path)
controldb = controlDB()
virustt = virustotal()

#
def getSampleTime ():
    file_path = 'configure.json'
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    sample_time = json_data["sampleTime"]
    return sample_time

#
def readFile():
    while True:
        try:
            with open(file_path, 'r') as file:
                file.seek(0, 2)
                while True:
                    line = file.readline()
                    if line:
                        print(line, end='')
                        management.separateData(line)
                    time.sleep(getSampleTime())
        except KeyboardInterrupt:
            print("\nstop")
            break

#
def pushURL_to_Virustotal(dict_temp):
    api_key = virustt.getJsonKey()
    
    dict_URL = management.filterURL(dict_temp)
    for log in dict_URL.values():
        scan_id = virustt.scan_url(log.URL,api_key)
        controldb.addValue(log,virustt.get_score(scan_id,api_key))

def main():
    readFile()
    dict_temp = management.filterDuplicateIP(management.proxy_logs)
    management.printTestIP()
    controldb.createTable()
    pushURL_to_Virustotal(dict_temp)

if __name__ == '__main__':
    main()