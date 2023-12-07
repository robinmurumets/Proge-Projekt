import requests
from bs4 import BeautifulSoup
import html5lib
headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36", 
        "Accept-Language": "en-US,en;q=0.9"
    }

def fetch_html_sisu_ja_soup(url):
    html_sisu = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_sisu.text, "html5lib")
    return html_sisu, soup

def hind(url, html_sisu, soup):
    hind = soup.find(attrs={"a-offscreen"}).get_text()
    if hind:
        return hind.strip()
    else:
        return "Hinda ei leitud"
    
def transport(url, html_sisu, soup):
    transport_hind = soup.find(attrs={"a-size-base a-color-secondary"}).get_text()
    
    return transport_hind.strip()

def nimi(url, html_sisu, soup):
    nimi = soup.find(id="productTitle").get_text()
    return nimi.strip()
    
    
def toote_url(toode):
    amazon_url = f"https://www.amazon.com/s?k={toode}"

    html_sisu, soup = fetch_html_sisu_ja_soup(amazon_url)

    
    lingid = []
    for product_div in soup.find_all("div", class_="a-section a-spacing-none puis-padding-right-small s-title-instructions-style"):
        link = product_div.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
        if link:
            lingid.append(f"https://www.amazon.com{link['href']}")

    return lingid




