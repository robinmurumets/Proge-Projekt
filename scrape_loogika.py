import requests
from bs4 import BeautifulSoup
import html5lib
headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36", 
        "Accept-Language": "en-US,en;q=0.9"
    }

url = "https://www.amazon.com/PlayStation-Console-Marvels-Spider-Man-Bundle-5/dp/B0CKZGY5B6/ref=sr_1_2?crid=1LIKSAPQ5C0UY&keywords=ps5&qid=1700577150&sprefix=%2Caps%2C269&sr=8-2"
html_sisu = requests.get(url, headers= headers)
soup = BeautifulSoup(html_sisu.text, "html5lib")
    
#Leiab toote hinna
def hind(url, html_sisu, soup):
    
    hind = soup.find(attrs={"a-offscreen"}).get_text()
      
    if hind:
        return hind.strip()
    else:
        return "Hinda ei leitud"

def nimi(url, html_sisu, soup):
    nimi = soup.find(id = "productTitle").get_text()
    
    return nimi.strip()
    
    
    
    

'''
def otsing():
    tooted = {}
    nimi = input("Sisestage toote nimi: ")
    url_teisendus = f"https://www.amazon.com/s?k={nimi.replace(' ', '+')}"
    
    tooted[nimi] = url_teisendus
'''
'''

    
'''


    
    
print(hind(url, html_sisu, soup))
print(nimi(url, html_sisu, soup))

    
    
    
    
    


#def pilt():


#def sisu():