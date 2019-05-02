list = (
    "http: // www.cct58.com / mneinv / 37520 / mx27 /",
    "http: // www.cct58.com / mneinv / 37796 / mx27 /",
    "http: // www.cct58.com / mneinv / 37707 / mx27 /",
    "http: // www.cct58.com / mneinv / 37521 / mx27 /",
    "http: // www.cct58.com / mneinv / 37522 / mx27 /",
    "http: // www.cct58.com / mneinv / 37419 / mx27 /",
    "http: // www.cct58.com / mneinv / 37523 / mx27 /",
    "http: // www.cct58.com / mneinv / 37525 / mx27 /",
    "http: // www.cct58.com / mneinv / 37526 / mx27 /",
    "http: // www.cct58.com / mneinv / 37365 / mx27 /",
    "http: // www.cct58.com / mneinv / 37470 / mx27 /",
    "http: // www.cct58.com / mneinv / 37530 / mx27 /",
    "http: // www.cct58.com / mneinv / 38571 / mx27 /",
    "http: // www.cct58.com / mneinv / 19631 / mx27 /",
    "http: // www.cct58.com / mneinv / 19558 / mx27 /",
    "http: // www.cct58.com / mneinv / 37531 / mx27 /",
    "http: // www.cct58.com / mneinv / 37535 / mx27 /",
    "http: // www.cct58.com / mneinv / 37536 / mx27 /",
    "http: // www.cct58.com / mneinv / 37538 / mx27 /",
    "http: // www.cct58.com / mneinv / 7141 / mx27 /",
    "http: // www.cct58.com / mneinv / 37426 / mx27 /",
    "http: // www.cct58.com / mneinv / 36599 / mx27 /",
    "http: // www.cct58.com / mneinv / 38565 / mx27 /",
    "http: // www.cct58.com / mneinv / 37527 / mx27 /",
    "http: // www.cct58.com / mneinv / 37539 / mx27 /",
    "http: // www.cct58.com / mneinv / 37540 / mx27 /",
    "http: // www.cct58.com / mneinv / 38566 / mx27 /",
    "http: // www.cct58.com / mneinv / 38560 / mx27 /",
    "http: // www.cct58.com / mneinv / 25610 / mx27 /",
    "http: // www.cct58.com / mneinv / 37291 / mx27 /")

print(len(list))
print(list[-2])

import requests
from bs4 import BeautifulSoup
def get_every_page():
    url = "http://www.cct58.com/mneinv/1.html"
    one_url_list = []
    html = requests.get(url).text
    soup = BeautifulSoup(html,'lxml')
    page_soup = soup.find('div',class_="text-c").find_all("a")
    last_page = int(page_soup[-2].text)
    for page_num in range(last_page):
        one_url = "http://www.cct58.com/mneinv/%d.html" % page_num
        one_url_list.append(one_url)
    return one_url_list


get_every_page()