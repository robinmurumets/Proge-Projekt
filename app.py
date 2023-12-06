import io
import tkinter as tk
from scrape_loogika import nimi, hind, fetch_html_sisu_ja_soup, transport

def fetch_hind():
    
    url = url_entry.get()
    
    html_sisu, soup = fetch_html_sisu_ja_soup(url)
    
    
    hind_value = hind(url, html_sisu, soup)
    nimi_value = nimi(url, html_sisu, soup)
    transport_value = transport(url, html_sisu, soup)
    
    label.config(text=f"{nimi_value}: {hind_value}; {transport_value}")
    


window = tk.Tk()
window.title("Amazonifier 3000")
window.geometry("800x800")


label = tk.Label(window, text="Toote info")
img_label = tk.Label(window)


url_entry = tk.Entry(window, width=40)
url_entry.insert(0, "")  


fetch_button = tk.Button(window, text="Leia toote info", command=fetch_hind)


label.pack(pady=10)
url_entry.pack(pady=5)
fetch_button.pack(pady=10)
img_label.pack(pady=10)


window.mainloop()