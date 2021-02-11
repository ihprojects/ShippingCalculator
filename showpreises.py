from tkinter import *
import shippingCalculator as sC
import parcelServiceOption as pSO

# Ereignisverarbeitung

def buttonVerarbeitenClick():
    listeAusgewaehlt = listboxNamen.curselection()
    itemAusgewaehlt = listeAusgewaehlt[0]
    nameAusgewaehlt = listboxNamen.get(itemAusgewaehlt)
    # Lass uns nach dem selektierten Anbieter suchen
    for anbieter in versandAnbieterPreise:
        if anbieter.name == nameAusgewaehlt:  
            # Wir haben den richtigen Anbieter gefunden 
            for i in range(len(anbieter.parcel_options)):
                preisOption = anbieter.parcel_options[i]
                Label(master=frameAusgabe, text = preisOption.name, bg='white').grid(row = i, column = 0)
                Label(master=frameAusgabe, text = preisOption.size_limit, bg='white').grid(row = i, column = 1)
                Label(master=frameAusgabe, text = preisOption.weight_limit, bg='white').grid(row = i, column = 2)
                Label(master=frameAusgabe, text = preisOption.price, bg='white').grid(row = i, column = 3)
                print(f"{preisOption.name}:{preisOption.size_limit}:{preisOption.weight_limit}:{preisOption.price}")
                # Statt print muss man in Listbox insert machen
            break;
        
    #labelText.config(text=textBegruessung)
    
versandAnbieterPreise = sC.get_price_services()

# Erzeugung des Fensters
tkFenster = Tk()
tkFenster.title('Preisliste')
tkFenster.geometry('500x600')
# Rahmen Listbox
frameListbox = Frame(master=tkFenster, bg='#FFCFC9')
frameListbox.place(x=5, y=5, width=330, height=160)
# Rahmen Ausgabe
frameAusgabe = Frame(master=tkFenster, bg='white') # , bg='#D5E88F'
frameAusgabe.place(x=5, y=170, width=330, height=100)
# Rahmen Verarbeitung
frameVerarbeitung = Frame(master=tkFenster, bg='#FBD975')
frameVerarbeitung.place(x=5, y=330, width=330, height=60)
# Kontrollvariable
text = StringVar()
# Listbox
listboxNamen = Listbox(master=frameListbox, selectmode='browse')
for anbieter in versandAnbieterPreise:
    listboxNamen.insert('end', anbieter.name)
listboxNamen.place(x=5, y=5, width=330, height=140)
# Label Text
# labelText = Label(master=frameAusgabe, bg='white')
# labelText.place(x=5, y=5, width=200, height=40)
# Button verarbeiten
buttonVerarbeiten = Button(master=frameVerarbeitung, text='Preise', command=buttonVerarbeitenClick)
buttonVerarbeiten.place(x=5, y=5, width=330, height=40)
# Aktivierung des Fensters
tkFenster.mainloop()
    


    
