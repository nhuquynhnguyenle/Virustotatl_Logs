#!/usr/bin/python
import os
import time
import subprocess
from ProxyLog import ProxyLog
from log_management import log_management

log_file = '/var/log/squid/access.log'
absolute_path = os.path.abspath(log_file)
proxy_logs = []
management = log_management(absolute_path)

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
    management.printInfo(management.proxy_logs)

if __name__ == '__main__':
    main()