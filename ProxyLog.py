#
class ProxyLog:
    
    #
    def __init__(self, time, port, ip, connection_type, size, method, url, contenttype, domain, destIP):
        self.Time = time
        self.Port = port
        self.IP = ip
        self.ConnectionType = connection_type
        self.Size = size
        self.Method = method
        self.URL = url
        self.ContentType = contenttype
        self.Domain = domain
        self.DestinateIP = destIP