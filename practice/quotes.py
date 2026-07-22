import httpx
from bs4 import BeautifulSoup
response= httpx.get("https://quotes.toscrape.com/")
print(response.status_code)
soup=BeautifulSoup(response.text, "html.parser")
quotes=soup.select(".quote")
for q in quotes:
    text=q.select_one(".text").text
    author=q.select_one(".author").text
    print(text)
    print(author)