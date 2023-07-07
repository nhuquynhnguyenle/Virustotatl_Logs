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
    def getDestIP(self, content):
        ip = content.split("/")[1]
        return ip
    
    
    def addLog_Data_Into_List(self,line):
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
            destIP = self.getDestIP(content_type)
            proxy_log = ProxyLog(time, port, ip, connection_type, size, method, url, content_type,domain,destIP)
            self.proxy_logs.append(proxy_log)
    
    #Method return the dictionary of logs have destination IP that is not duplicated
    def getUnique_IP_Log(self, proxy_logs):
        dict_logs = {}
        for log in proxy_logs:
            destIP = log.DestinateIP
            if destIP not in dict_logs:
                dict_logs[destIP] = log
        return dict_logs
    
    #
    def filterURL(self,dict_logs):
        temp_dict={}
        for key, log in dict_logs.items():
            if log.Method == "GET" or log.Method == "POST":
                temp_dict[key] = log 
        return temp_dict
    
    #
    def printInfo(self,logs):
        for proxy_log in logs.values():
            print(f"\nPort: {proxy_log.Port}\nSource Ip: {proxy_log.IP}\nConnect: {proxy_log.ConnectionType}\nMethod: {proxy_log.Method}\nURL: {proxy_log.URL}\nContent: {proxy_log.ContentType}\nDomain: {proxy_log.Domain}\nDestination IP: {proxy_log.DestinateIP}")
    
    #
    def writeAccess_Log_Into_File(self,log,score):
        if score >= 10 :
            with open(".detect", "a") as f:
                f.write(f"\nTime: {log.Time} - Source IP: {log.IP} -  Destination IP: {log.DestinateIP} - Port: {log.Port} - Method: {log.Method} - URL: {log.URL} - Domain: {log.Domain} - Score: {score}")

