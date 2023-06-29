#!/usr/bin/python
import os
import time
import subprocess
from ProxyLog import ProxyLog

log_file = '/var/log/squid/access.log'
absolute_path = os.path.abspath(log_file)
proxy_logs = []

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
                separateData(line)
            except KeyboardInterrupt:
                process.kill()
                break
    except FileNotFoundError:
        print("File not found")
    except PermissionError:
        print("Permission denied")

def separateData(line):
    parts = line.split()
    if len(parts) >= 9:
        time = parts[0]
        port = parts[1]
        ip = parts[2]
        connection_type = parts[3]
        size = parts[4]
        method = parts[5]
        url = parts[6]
        content_type = parts[8]
        proxy_log = ProxyLog(time, port, ip, connection_type, size, method, url, content_type)
        proxy_logs.append(proxy_log)

def printInfo(logs):
    for proxy_log in logs:
        print(f"\nPort: {proxy_log.Port}\nIp: {proxy_log.IP}\nConnect: {proxy_log.ConnectionType}\nMethod: {proxy_log.Method}\nURL: {proxy_log.URL}\nContent: {proxy_log.ContentType}")

readFile()
printInfo(proxy_logs)