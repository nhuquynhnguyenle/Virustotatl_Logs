import time
from ProxyLog import ProxyLog

file_path = 'access.log'
proxy_logs = []

#Method reading line in
def readFile():
    while True:
        try:
            with open(file_path, 'r') as file:
                file.seek(0, 2)
                while True:
                    line = file.readline()
                    if line:
                        print(line, end='')
                        separateData(line)
                    time.sleep(0.2)
        except KeyboardInterrupt:
            print("\nstop")
            break

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