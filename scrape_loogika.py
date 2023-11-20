import requests
from bs4 import BeautifulSoup

#Leiab toote hinna
def hind(url):
    
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0", 
        "Accept-Language": "en-US,en;q=0.5"
    }
    
    html_sisu = requests.get(url, headers)
    soup = BeautifulSoup(html_sisu.text, "lxml")
    
    hind = soup.select_one("span.a-price-whole.#text")
    
    if hind:
        return f"Hind: {hind.text.strip()} "
    else:
        return "Hinda ei leitud"
    

'''
def otsing():
    tooted = {}
    nimi = input("Sisestage toote nimi: ")
    url_teisendus = f"https://www.amazon.com/s?k={nimi.replace(' ', '+')}"
    
    tooted[nimi] = url_teisendus
'''
'''
def nimi(url):
    
'''


    
    
print(hind("https://www.amazon.com/LKV-Womens-Winter-Casual-Christmas/dp/B0CB45ZFY3/ref=sr_1_24?crid=Y6I1E8KZNFCA&keywords=christmas%2Bgift&qid=1700512236&sprefix=christmas%2Bgift%2Caps%2C225&sr=8-24&th=1&psc=1"))
    
    
    
    
    
    


#def pilt():


#def sisu():