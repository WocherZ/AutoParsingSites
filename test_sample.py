from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()

url = "https://fortis-development.ru/flats?result_mode=0&complex_visual_mode=0&property_visual_mode=1&is_free=1&complex=1"

r = session.get(url)

r.html.render()

soup = BeautifulSoup(r.html.html, "lxml")

tags = soup.find_all(class_="container")
for tag in tags:
    print(tag)

print("Successfully end!")
