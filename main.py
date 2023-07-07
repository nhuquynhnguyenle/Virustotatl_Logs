import time
from log_management import log_management
import json
import os
import sys
import sqlite3
from ControlDB import controlDB
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
def readFile(file_path):
    last_modified = os.path.getmtime(file_path)
    timeout = 30  
    elapsed_time = 0 
    while True:
        try:
            with open(file_path, 'r') as file:
                file.seek(0, 2)
                while True:
                    line = file.readline()
                    if line:
                        print(line, end='')
                        management.addLog_Data_Into_List(line)
                    
                    current_modified = os.path.getmtime(file_path)
                    if current_modified != last_modified:
                        last_modified = current_modified
                        elapsed_time = 0  

                    time.sleep(getSampleTime())
                    elapsed_time += getSampleTime()
                    
                    if elapsed_time >= timeout:
                        print("File not changed within the timeout. Exiting program.")
                        sys.exit()
        
        except KeyboardInterrupt:
            print("\n")
            break
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
            return True

#
def getCursorAndConnect():
    try:
        connect = sqlite3.connect('Test.db')
        cursor = connect.cursor()
        print("Connection and cursor created successfully")
        return connect,cursor
    except sqlite3.Error as e:
        print("Error connecting to database:", str(e))

#
def checkAlert(dict_logs):
    for log in dict_logs.values():
        if alertDangerDomain(log.Domain) != True:
            return "\nDangerous domain access not found."
        else:
            return f"\nAlert: Have access into {log.Domain}"

def main():
    readFile(file_path)
    connect,cursor = getCursorAndConnect()
    controldb.createTable(cursor)
    dict_logs = getDictionaryLogs()
    management.printInfo(dict_logs)
    api_key = virustt.getJsonKey()
    for log in dict_logs.values():
        scan_id = virustt.scan_url(log.URL,api_key)
        score = virustt.get_score(scan_id,api_key)
        controldb.addValue(log,score,cursor)
        management.writeAccess_Log_Into_File(log,score)
    print(checkAlert(dict_logs))
    connect.commit()
    connect.close()
    
if __name__ == '__main__':
    main()