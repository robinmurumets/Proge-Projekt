import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk
import requests
import io
from scrape_loogika import nimi, hind, transport, toote_url, fetch_html_sisu_ja_soup, pildi_url, salvesta_andmed
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import pandas as pd

window = tk.Tk()
taustavärv = "#1D212B"
window.title("Amazoni Tooteotsija")
window.state("zoomed")
window.configure(bg=taustavärv)

pildid = []

def kuva_graafik(toote_nimi):
    df = pd.read_csv('toote_ajalugu.csv', names=['Nimi', 'Hind', 'Transport', 'Aeg'])
    df['Aeg'] = pd.to_datetime(df['Aeg'], errors='coerce') 
    df['Hind'] = pd.to_numeric(df['Hind'].replace('[\€\$\,]', '', regex=True), errors='coerce')
    filtreeritud_df = df[df['Nimi'] == toote_nimi]

    figure = Figure(figsize=(5, 4), dpi=100)
    joonis = figure.add_subplot(111)
    joonis.plot(filtreeritud_df['Aeg'], filtreeritud_df['Hind'])

    joonis.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    joonis.xaxis.set_major_locator(mdates.DayLocator())
    figure.autofmt_xdate()

    graafika_window = tk.Toplevel(window)
    graafika_window.title(f"Hinnagraafik - {toote_nimi}")
    graafik = FigureCanvasTkAgg(figure, master=graafika_window)
    graafik_widget = graafik.get_tk_widget()
    graafik_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    graafik.draw()

def hangi_toote_info():
    global pildid
    pildid.clear()
    toote_nimi = toote_sisestus.get()
    for widget in toote_containers_window.winfo_children():
        widget.destroy()

    toote_lingid = toote_url(toote_nimi)
    for link in toote_lingid:
        html_sisu, soup = fetch_html_sisu_ja_soup(link)
        hinna_väärtus, ajatempel = hind(link, html_sisu, soup)
        nime_väärtus, _ = nimi(link, html_sisu, soup)
        transpordi_väärtus, _ = transport(link, html_sisu, soup)
        pildi_urlid = pildi_url(link, html_sisu, soup)
    

        if pildi_urlid and hinna_väärtus:
            product_name_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
            toote_container = tk.Frame(toote_containers_window, bg=taustavärv, borderwidth=0, highlightthickness=0)
            toote_container.pack(fill=tk.X, pady=10)

            pildi_andmed = requests.get(pildi_urlid).content
            pilt = Image.open(io.BytesIO(pildi_andmed))
            pilt.thumbnail((150, 150))
            foto = ImageTk.PhotoImage(pilt)
            pildi_margis = tk.Label(toote_container, image=foto, bg=taustavärv, borderwidth=0, highlightthickness=0)
            pildi_margis.image = foto
            pildi_margis.pack(side=tk.LEFT, padx=10)

            product_name_label = tk.Label(toote_container, text=nime_väärtus, font=product_name_font, bg=taustavärv, fg="White")
            product_name_label.pack(side=tk.TOP, padx=10, anchor='w')

            details_label = tk.Label(toote_container, text=f"hinna_väärtus: {hinna_väärtus}\nKohaletoimetamine: {transpordi_väärtus}", justify=tk.LEFT, bg=taustavärv, fg="White")
            details_label.pack(side=tk.TOP, padx=10, anchor='w')

            price_history_button = tk.Button(toote_container, text="Vaata hinnalugu", command=lambda nimi=nime_väärtus: kuva_graafik(nime_väärtus), bg=taustavärv, fg="white")
            price_history_button.pack(side=tk.LEFT, padx=10)

            salvesta_andmed(nime_väärtus, hinna_väärtus, transpordi_väärtus, ajatempel)
            pildid.append(foto)



sisestuse_window = tk.Frame(window, bg=taustavärv, borderwidth=0, highlightthickness=0)
sisestuse_window.pack(pady=5, anchor='w')

toote_sisestus = tk.Entry(sisestuse_window, width=50, borderwidth=0)
toote_sisestus.pack(side=tk.LEFT, padx=10, anchor='w')

hangi_nupp = tk.Button(sisestuse_window, text="Hangi Toote Info", command=hangi_toote_info, bg=taustavärv, fg="white", borderwidth=0, highlightthickness=0)
hangi_nupp.pack(side=tk.LEFT, padx=10)


toote_window = tk.Canvas(window, bg=taustavärv, borderwidth=0, highlightthickness=0)
scrollbar = tk.Scrollbar(window, orient="vertical", command=toote_window.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

toote_window.configure(yscrollcommand=scrollbar.set)
toote_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

toote_containers_window = tk.Frame(toote_window, bg=taustavärv)
toote_window.create_window((0, 0), window=toote_containers_window, anchor='nw')

def onFrameConfigure(event):
    toote_window.configure(scrollregion=toote_window.bbox("all"))

toote_containers_window.bind("<Configure>", onFrameConfigure)

def onMouseWheel(event):
    toote_window.yview_scroll(-1 * int((event.delta / 120)), "units")

window.bind_all("<MouseWheel>", onMouseWheel)

window.mainloop()
