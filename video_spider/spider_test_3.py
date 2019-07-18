import requests

url = "https://cd15-c120-1.play.bokecc.com/flvs/cb/QxEm3/hoyHT3inXd-0.pcf?t=1560505573&key=E8BAF5D6E9B97F1338962F118A615B4B&tpl=10&tpt=111&upid=3558291560498373481&pt=0&pi=1&time_random=1560498374989_769630"

response = requests.get(url)
with open("a.mp4", 'wb') as f:
    f.write(response.content)
