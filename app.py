import io
import tkinter as tk
from loogika import nimi, hind, fetch_html_sisu_ja_soup, transport, toote_url

def fetch_product_info():
    url = toode.get()

    try:
        product_links = toote_url(url)

        for link in product_links:
            try:
                html_sisu, soup = fetch_html_sisu_ja_soup(link)
                hind_value = hind(link, html_sisu, soup)
                nimi_value = nimi(link, html_sisu, soup)
                transport_value = transport(link, html_sisu, soup)

                label.config(text=f"{nimi_value}: {hind_value}; {transport_value}")
            except Exception as e:
                # Handle the exception (e.g., log it) or simply pass
                pass

    except Exception as e:
        label.config(text=f"Error: {str(e)}")


window = tk.Tk()
window.title("Amazonifier 3000")
window.geometry("800x800")


img_label = tk.Label(window)

toode = tk.Entry(window, width=40)
toode.insert(0, "")

fetch_button = tk.Button(window, text="Leia toote info", command=fetch_product_info)


label = tk.Label(window, text="Toote info")

label.pack(pady=10)
toode.pack(pady=5)
fetch_button.pack(pady=10)
img_label.pack(pady=10)

window.mainloop()
