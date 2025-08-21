# Jozef Korchňák III.A 2025/2026
# Hádanie náhodného slova z listu s grafickým výpisom

import tkinter as tk
import random
from datetime import datetime

slova = ["program", "python", "klavesnica", "monitor", "kalkulacka",
         "sustava", "robotika", "elektrina", "siet", "pamäť"]

pokusy = 0
skore = [0, 0]
hrac_na_rade = 0
mod = 1
anagram = ""
spravne_slovo = ""
vstup = None
canvas = None
meno_hraca = ["Hráč 1", "Hráč 2"]

def zamiesaj_slovo(slovo):
    return ''.join(random.sample(slovo, len(slovo)))

def nove_kolo():
    global spravne_slovo, anagram
    spravne_slovo = random.choice(slova)
    anagram = zamiesaj_slovo(spravne_slovo)
    aktualizuj_canvas()

def vyhodnot():
    global pokusy, hrac_na_rade
    tip = vstup.get().strip().lower()
    if tip == spravne_slovo:
        skore[hrac_na_rade] += 1
        farba = "green"
    else:
        farba = "red"

    canvas.create_text(250, 250 + pokusy * 25,
                       text=f"{meno_hraca[hrac_na_rade]} tipol: {tip} "
                            f"({'spravne' if tip == spravne_slovo else 'zle'})",
                       font=('Arial', 12), fill=farba)

    pokusy += 1
    hrac_na_rade = 1 - hrac_na_rade if mod == 2 else hrac_na_rade

    if pokusy >= (3 if mod == 1 else 6):
        ukonci_hru()
    else:
        nove_kolo()

def ukonci_hru():
    vysledok = f"Hra skončila! {meno_hraca[0]}: {skore[0]} bodov"
    if mod == 2:
        vysledok += f", {meno_hraca[1]}: {skore[1]} bodov"

    canvas.create_text(250, 400, text=vysledok, font=('Arial', 15, 'bold'))
    uloz_historiu()
    restart_btn = tk.Button(text="Hrať znova", command=reset)
    restart_btn.pack()
    btn.destroy()

def uloz_historiu():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("historia.txt", "a", encoding="utf-8") as subor:
        riadok = f"{now} - {meno_hraca[0]}: {skore[0]}"
        if mod == 2:
            riadok += f", {meno_hraca[1]}: {skore[1]}"
        subor.write(riadok + "\n")

def aktualizuj_canvas():
    canvas.delete("anagram")
    canvas.create_text(250, 150, text=f"Uhádni slovo: {anagram}",
                       font=('Arial', 20, 'bold'), tags="anagram")

def spusti_hru(zvoleny_mod):
    global mod, canvas, vstup,btn
    mod = zvoleny_mod

    for widget in tk._default_root.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(width=500, height=500)
    canvas.pack()
    vstup = tk.Entry(width=20)
    vstup.pack()
    btn = tk.Button(text="Odoslať", command=vyhodnot)
    btn.pack()
    canvas.create_text(250, 50, text="Hádanie anagramu",
                       font=('Arial', 25, 'bold'))
    nove_kolo()

def reset():
    global pokusy, skore, hrac_na_rade
    pokusy = 0
    skore = [0, 0]
    hrac_na_rade = 0
    rozhranie()

def rozhranie():
    for widget in tk._default_root.winfo_children():
        widget.destroy()

    uvod = tk.Canvas(width=500, height=500)
    uvod.pack()
    uvod.create_text(250, 100, text='Hra sa začína!',
                     font=('Arial', 25, 'bold'))
    uvod.create_text(250, 150, text='Vyber si mód hry',
                     font=('Arial', 15, 'bold'))

    uvod.create_rectangle(100, 240, 400, 310, fill="")
    uvod.create_rectangle(100, 330, 400, 400, fill="")

    t1 = uvod.create_text(250, 275, text='Hra pre jedného hráča',
                          font=('Arial', 20, 'bold'))
    t2 = uvod.create_text(250, 365, text='Hra pre dvoch hráčov',
                          font=('Arial', 20, 'bold'))

    uvod.tag_bind(t1, "<Button-1>", lambda e: spusti_hru(1))
    uvod.tag_bind(t2, "<Button-1>", lambda e: spusti_hru(2))

# Spustenie programu
tk.Tk().title("Anagramová hra")
rozhranie()
tk.mainloop()
