from tkinter import *
import shippingCalculator as sC
import parcelServiceOption as pSO

# Ereignisverarbeitung

def buttonVerarbeitenClick():
    listeAusgewaehlt = listboxNamen.curselection()
    itemAusgewaehlt = listeAusgewaehlt[0]
    nameAusgewaehlt = listboxNamen.get(itemAusgewaehlt)
    textBegruessung = 'Hallo ' + nameAusgewaehlt +'!'
    # Lass uns nach dem selektierten Anbieter suchen
    for anbieter in versandAnbieterPreise:
        if anbieter.name == nameAusgewaehlt:  
            # Wir haben den richtigen Anbieter gefunden 
            for preisOption in anbieter.parcel_options:
                # TODO show priceOption in grid
                print(f"{preisOption.name}:{preisOption.size_limit}:{preisOption.weight_limit}:{preisOption.price}")
                # Statt print muss man in Listbox insert machen
            break;
        
    labelText.config(text=textBegruessung)

def show_price_window(versandAnbieterPreise):
    # Erzeugung des Fensters
    tkFenster = Tk()
    tkFenster.title('Test')
    tkFenster.geometry('120x160')
    # Rahmen Listbox
    frameListbox = Frame(master=tkFenster, bg='#FFCFC9')
    frameListbox.place(x=5, y=5, width=110, height=80)
    # Rahmen Ausgabe
    frameAusgabe = Frame(master=tkFenster, bg='#D5E88F')
    frameAusgabe.place(x=5, y=90, width=110, height=30)
    # Rahmen Verarbeitung
    frameVerarbeitung = Frame(master=tkFenster, bg='#FBD975')
    frameVerarbeitung.place(x=5, y=125, width=110, height=30)
    # Kontrollvariable
    text = StringVar()
    # Listbox
    listboxNamen = Listbox(master=frameListbox, selectmode='browse')
    for anbieter in versandAnbieterPreise:
        listboxNamen.insert('end', anbieter.name)
    listboxNamen.place(x=5, y=5, width=100, height=70)
    # Label Text
    # TODO: change labelText to grid
    labelText = Label(master=frameAusgabe, bg='white')
    labelText.place(x=5, y=5, width=100, height=20)
    # Button verarbeiten
    buttonVerarbeiten = Button(master=frameVerarbeitung, text='begrüßen', command=buttonVerarbeitenClick)
    buttonVerarbeiten.place(x=5, y=5, width=100, height=20)
    # Aktivierung des Fensters
    tkFenster.mainloop()
    

if __name__ == '__main__':
    versandAnbieterPreise = sC.get_price_services()
    show_price_window(versandAnbieterPreise)