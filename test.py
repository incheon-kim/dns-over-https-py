import asyncio
from DNSoverHTTPS import DNSoverHTTPS

# test code 
d = DNSoverHTTPS()

# create tasks
target_url = ["pornhub.com", "naver.com", "xvideos.com", "daum.net", "google.com", "nexon.com", "dogdrip.net", "cloudflare.com", "faketesturl.net"]
tasks = [d.lookup(x) for x in target_url]

# run asynchronously
asyncio.run(asyncio.wait(tasks))
