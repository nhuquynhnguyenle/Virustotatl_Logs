#!/usr/bin/python
import os
import time
import subprocess
import time
import json
from log_management import log_management
from ControlDB import controlDB
from virustotal import virustotal

log_file = '/var/log/squid/access.log'
absolute_path = os.path.abspath(log_file)

management = log_management(absolute_path)
controldb = controlDB()
virustt = virustotal()

def getSampleTime ():
    file_path = 'configure.json'
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    sample_time = json_data["sampleTime"]
    return sample_time

#
def readFile():
    try:
        process = subprocess.Popen(['tail', '-f', absolute_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            try:
                line = process.stdout.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                #print(line.decode().strip())
                management.separateData(line)
            except KeyboardInterrupt:
                process.kill()
                break
    except FileNotFoundError:
        print("File not found")
    except PermissionError:
        print("Permission denied")

#
def getDictionaryLogs():
    dict_logs = management.getUnique_IP_Log(management.proxy_logs)
    dict_logs = management.filterURL(dict_logs)
    return dict_logs

#
def alertDangerDomain(domain):
    with open(".manual", "r") as f:
        monitored_domain = f.read().splitlines()
        if domain in monitored_domain:
            return f"Alert: Have access into {domain}"



def main():
    readFile()
    dict_logs = getDictionaryLogs()
    management.printInfo(dict_logs)
    api_key = virustt.getJsonKey()
    for log in dict_logs.values():
        scan_id = virustt.scan_url(log.URL,api_key)
        score = virustt.get_score(scan_id,api_key)
        management.writeAccess_Log_Into_File(log,score)
        print(alertDangerDomain(log.domain))

if __name__ == '__main__':
    main()