import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime
import csv

def fetch_html_sisu_ja_soup(url):
    session = requests.Session()
    html_sisu = session.get(url, headers=headers)
    soup = BeautifulSoup(html_sisu.text, "lxml")
    return html_sisu, soup

def hind(url, html_sisu, soup):
    price_containers = soup.find_all("span", class_="a-price")

    for container in price_containers:
        price = container.find("span", class_="a-offscreen")
        if price:
            return price.get_text().strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return "Hinda ei leitud", datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def transport(url, html_sisu, soup):
    transport_hind = soup.find(class_={"a-size-base a-color-secondary"}).get_text()
    return transport_hind.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def nimi(url, html_sisu, soup):
    nimi_elem = soup.find("span", id="productTitle")
    return nimi_elem.get_text().strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def toote_url(toode):
    amazon_url = f"https://www.amazon.com/s?k={toode}"
    html_sisu, soup = fetch_html_sisu_ja_soup(amazon_url)
    lingid = []

    product_divs = soup.find_all("div", class_="a-section a-spacing-none puis-padding-right-small s-title-instructions-style")
    for product_div in product_divs[:10]:
        link = product_div.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
        if link:
            lingid.append(f"https://www.amazon.com{link['href']}")

    if not lingid:
        product_divs = soup.find_all("div", class_="s-product-image-container aok-relative s-text-center s-image-overlay-grey puis-image-overlay-grey s-padding-left-small s-padding-right-small puis-spacing-small s-height-equalized puis puis-v1tjwq006lh4w12552icvhgwd84")
        for product_div in product_divs[:10]:
            link = product_div.find("a", class_="a-link-normal s-no-outline")
            if link:
                lingid.append(f"https://www.amazon.com{link['href']}")

    return lingid


def pildi_url(url, html_sisu, soup):
    img_tag = soup.find("img", id="landingImage")
    if img_tag and 'src' in img_tag.attrs:
        return img_tag['src']
    else:
        return None

def salvesta_andmed(toote_nimi, hind, transport_hind, ajatempel):
    with open('toote_ajalugu.csv', mode='a', newline='', encoding='utf-8') as fail:
        kirjutaja = csv.writer(fail)
        kirjutaja.writerow([toote_nimi, hind, transport_hind, ajatempel])


print(toote_url("https://www.amazon.com/s?k=versace"))

