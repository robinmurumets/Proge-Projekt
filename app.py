import tkinter as tk
from tkinter import Canvas, Scrollbar, Toplevel
from PIL import Image, ImageTk
import requests
import io
from scrape_loogika import nimi, hind, transport, toote_url, fetch_html_sisu_ja_soup, pildi_url, salvesta_andmed
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

pildi_viited = []
toote_nimed = []

def uuenda_toote_valikumenyy():
    menyy = toote_valik["menu"]
    menyy.delete(0, "end")
    for nimi in toote_nimed:
        menyy.add_command(label=nimi, command=lambda value=nimi: valitud_toode.set(value))

def hangi_toote_info():
    global pildi_viited, toote_nimed
    pildi_viited.clear()
    toote_nimed.clear()
    toote_nimi = toote_sisestus.get()
    for vidin in toote_konteinerid_aken.winfo_children():
        vidin.destroy()
    try:
        toote_lingid = toote_url(toote_nimi)
        for link in toote_lingid:
            html_sisu, soup = fetch_html_sisu_ja_soup(link)
            hind_vaartus, ajatempel = hind(link, html_sisu, soup)
            nimi_vaartus, _ = nimi(link, html_sisu, soup)
            transport_vaartus, _ = transport(link, html_sisu, soup)
            pildi_url_väärtus = pildi_url(link, html_sisu, soup)
            toote_nimed.append(nimi_vaartus)
            if pildi_url_väärtus and hind_vaartus:
                toote_konteiner = tk.Frame(toote_konteinerid_aken, bg=taustavärv, borderwidth=0,highlightthickness=0)
                toote_konteiner.pack(fill=tk.X, pady=10)
                pildi_andmed = requests.get(pildi_url_väärtus).content
                pilt = Image.open(io.BytesIO(pildi_andmed))
                pilt.thumbnail((150, 150))
                foto = ImageTk.PhotoImage(pilt)
                pildi_margis = tk.Label(toote_konteiner, image=foto, bg=taustavärv, borderwidth=0,highlightthickness=0)
                pildi_margis.image = foto
                pildi_margis.pack(side=tk.LEFT, padx=10)
                info_tekst = f"{nimi_vaartus}\nHind: {hind_vaartus}\nKohaletoimetamine: {transport_vaartus}"
                info_margis = tk.Label(toote_konteiner, text=info_tekst, justify=tk.LEFT, bg=taustavärv, fg="White", borderwidth = 0, highlightthickness= 0)
                info_margis.pack(side=tk.LEFT, padx=10)
                salvesta_andmed(nimi_vaartus, hind_vaartus, transport_vaartus, ajatempel)
                pildi_viited.append(foto)
        uuenda_toote_valikumenyy()
        toote_aken.update_idletasks()
        toote_aken.config(scrollregion=toote_aken.bbox("all"))
    except Exception as e:
        viga_margis.config(text=f"Viga: {str(e)}")

def kuva_graafik(toote_nimi):
    df = pd.read_csv('toote_ajalugu.csv', names=['Nimi', 'Hind', 'Transport', 'Aeg'])
    df['Aeg'] = pd.to_datetime(df['Aeg'])
    df['Hind'] = pd.to_numeric(df['Hind'].replace('[\€\$\,]', '', regex=True), errors='coerce')
    filtreeritud_df = df[df['Nimi'] == toote_nimi]
    figuur = Figure(figsize=(5, 4), dpi=100)
    joonis = figuur.add_subplot(111)
    joonis.plot(filtreeritud_df['Aeg'], filtreeritud_df['Hind'])
    graafika_aken = tk.Toplevel(window)
    graafika_aken.title("Hinnagraafik")
    canvas = FigureCanvasTkAgg(figuur, master=graafika_aken)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.draw()

window = tk.Tk()
taustavärv = "#1D212B"
tekstivärv = "#d67b04"
window.title("Amazoni Tooteotsija")
window.state("zoomed")
window.configure(bg=taustavärv,borderwidth=0,highlightthickness=0)

sisestuse_aken = tk.Frame(window, bg=taustavärv, borderwidth=0,highlightthickness=0)
sisestuse_aken.pack(pady=5)

toote_sisestus = tk.Entry(sisestuse_aken, width=50)
toote_sisestus.pack(side=tk.LEFT, padx=10)

toote_aken = tk.Canvas(window, bg=taustavärv, borderwidth=0,highlightthickness=0)
scrollbar = tk.Scrollbar(window, command=toote_aken.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
toote_aken.config(yscrollcommand=scrollbar.set)
toote_aken.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

toote_konteinerid_aken = tk.Frame(toote_aken, bg=taustavärv, borderwidth=0,highlightthickness=0)
toote_aken.create_window((0, 0), window=toote_konteinerid_aken, anchor='nw')

graafika_nupp = tk.Button(window, text="Näita graafikut", command=lambda: kuva_graafik(valitud_toode.get()), bg=taustavärv, fg="White", borderwidth=0,highlightthickness=0)
hangi_nupp = tk.Button(sisestuse_aken, text="Hangi Toote Info", command=hangi_toote_info, bg=taustavärv, fg="white", borderwidth=0,highlightthickness=0)

viga_margis = tk.Label(window, text="", bg=taustavärv, borderwidth=0,highlightthickness=0)

valitud_toode = tk.StringVar(window)
valitud_toode.set("Vali toode")
toote_valik = tk.OptionMenu(window, valitud_toode, toote_nimed)
toote_valik.config(bg=taustavärv, fg="white", borderwidth=0,highlightthickness=0)

toote_aken.pack(fill=tk.BOTH, expand=True)
viga_margis.pack()
hangi_nupp.pack(side=tk.LEFT, padx=10)
toote_valik.pack()
graafika_nupp.pack()

window.mainloop()
