from bs4 import BeautifulSoup
with open ("home.html","r") as file:
    html=file.read()
soup=BeautifulSoup(html,"html.parser")
product=soup.select_one(".product")
name=product.select_one("h2").text
price=product.select_one("span").text
print(name)
print(price)
