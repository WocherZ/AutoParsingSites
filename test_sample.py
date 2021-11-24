from requests_html import HTMLSession, AsyncHTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()
# asession = AsyncHTMLSession()
# url = "https://fortis-development.ru/flats?result_mode=0&complex_visual_mode=0&property_visual_mode=1&is_free=1&complex=1"
url = "https://osnova-house.ru/catalog/?choose=list&floor[0]=1&floor[1]=15&price[0]=3671600&price[1]=16000000&turn=4"

r = session.get(url)

r.html.render()

print(type(r.html), type(r.html.html))
print(r.html)
#
# req = asession.get(url)
#
# req.html.arender()
#
# print(req.html.html)




# soup = BeautifulSoup(r.html.html, "lxml")
#
# tags = soup.find_all(class_="container")
# for tag in tags:
#     print(tag)
#
# print("Successfully end!")
