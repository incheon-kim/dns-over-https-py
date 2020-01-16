import json
import ipaddress
import aiohttp
import asyncio

# Asynchronous DNS-over-HTTPS

HTTPS = "https://"

DNS_SERVER = {
    "CLOUDFLARE" : {
        'URL' : 'cloudflare-dns.com',
        'PATH' : '/dns-query',
        'ct' : 'application/dns-json'

    },
    "GOOGLE": {
        'URL' : '8.8.4.4',
        'PATH' : "/dns-query",
        'ct' : "application/dns-message"
    }
}

class DNSoverHTTPS:
    def __init__(self, server=True):
        # True - CloudFlare(1.1.1.1) False - Google(8.8.4.4)
        self.server = server
        
    # check given string is ip or not
    def isIP(self, ip):
        try:
            return bool(ipaddress.ip_address(ip))
        except ValueError:
            return false

    async def lookup(self, hostname):
        addresses = await self.requestToDNS(hostname)
        ip = None
        try:
            for dest in addresses:
                if self.isIP(dest):
                    ip = dest
                    print(hostname, dest)
                    return ip
                if ip is None:
                    # if data does not IPv4 format.
                    raise ValueError("Invalid IP")
        except (ValueError, TypeError) as e:
                if e.__class__.__name__ == "TypeError":
                    print("lookup > '", hostname, "' DNS look up failed. Looks like it doesn't exist")
                if e.__class__.__name__ == "ValueError":
                    print("lookup > ", str(e))
                return ip
    
    async def buildGETquery(self, url, query):
        # build GET query URL from url and query dict.
        url = url + '?'
        for i, (k, v) in enumerate(query.items()):
            url = url + k + '=' + v
            if i is not 2:
                url = url + '&'
        return url    

    async def requestToDNS(self, hostname, dnsserver=True, querytype="A"):
        # querytype 'A' returns IPv4 address
        # querytype 'AAAA' returns IPv6 address (not available in Korea)
        destination = None
        
        # GET queries
        dnsquery = {
            "name": hostname,
            "type" : querytype,
            "ct" : None
        }

        if dnsserver is True:
            #CLOUDFLARE
            destination = "CLOUDFLARE"
        else:
            #GOOGLE DNS
            destination = "GOOGLE"
        
        url = HTTPS + DNS_SERVER[destination]['URL'] + DNS_SERVER[destination]['PATH']
        dnsquery['ct'] = DNS_SERVER[destination]['ct']

        async with aiohttp.ClientSession() as sess:
            async with sess.get(await self.buildGETquery(url, dnsquery)) as response:                
                res = await response.read()
                content = json.loads(res.decode())
                if "Answer" in content.keys():
                    ip_addresses = [x['data'] for x in content['Answer']]
                else:
                    ip_addresses = None

                return ip_addresses