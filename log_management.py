from ProxyLog import ProxyLog
from urllib.parse import urlparse

#
class log_management:
    
    #
    def __init__(self, file_path):
        self.file_path = file_path
        self.proxy_logs = [] 
    
    #
    def getDomain(self,url):
        if url.startswith("http://") or url.startswith("https://"):
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
        else:
            domain = url.split(":")[0]
        return domain
    
    #
    def separateData(self,line):
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
            domain = self.getDomain(url)
            proxy_log = ProxyLog(time, port, ip, connection_type, size, method, url, content_type,domain)
            self.proxy_logs.append(proxy_log)

    #
    def printInfo(self,logs):
        for proxy_log in logs:
            print(f"\nPort: {proxy_log.Port}\nIp: {proxy_log.IP}\nConnect: {proxy_log.ConnectionType}\nMethod: {proxy_log.Method}\nURL: {proxy_log.URL}\nContent: {proxy_log.ContentType}\nDomain: {proxy_log.Domain}")