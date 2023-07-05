#!/usr/bin/python
import os
import time
import subprocess
from ProxyLog import ProxyLog
from log_management import log_management
import json
from virustotalDB import controlDB
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

def main():
    readFile()

if __name__ == '__main__':
    main()