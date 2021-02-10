from classes import ParcelService, ParcelOption, Package
from datetime import date, timedelta


#TODO implement csv reader 
infos = [
     {'options' : {'Päckchen S':[(35,25,10),2,3.79,'n'],'Päckchen M':[(60,30,15),2,4.39,'n']
     , 'Paket S':[(60,30,15),2,4.99,'n'], 'Paket M':[(120,60,60),5,5.99,'n']}, 'calc_style': 1
     ,'name': 'DHL', 'delivery_time': 3}
    ,{'options':{'XS':[(35,),1000,3.90,'n'],'S':[(50,),1000,4.20,'n'],'M' :[(70,),1000,6.60,'n']}
    , 'calc_style': 1,'name': 'DPD', 'delivery_time': 3}
    ,{'options' :{'Hermes Päckchen': [(37,),25,4.50,'n'],'XL-Paket':[(150,),31.5,28.95,'n']}
    , 'calc_style' : 2,'name': 'Hermes', 'delivery_time': 4}
    ]


def create_package():
    """Erstellt ein neues Paket"""
    print('Bitte geben Sie die Paketmaße in cm ein')
    L = int(input('Länge: '))
    W = int(input('Breite: '))
    H = int(input('Höhe: '))
    weight = int(input('Gewicht in kg: '))

    return Package(sorted([L,W,H],reverse=True),weight)
    

def show_help():
    print('\nSie können die folgenden Befehle verwenden:\n')
    commands={'q': 'verlässt das Programm'
        ,'about' : 'Informationen über dieses Programm'
        ,'new' : create_package.__doc__
        ,'prices' : show_prices.__doc__
        ,'best' : 'zeigt die günstigsten Versandoptionen'
        ,'delivery' : 'voraussichtliches Lieferdatum'
        }
    for i in commands.items():
        print(f'{i[0] :20}\t{i[1]}')


def show_prices(parcel_services):
    """Gibt die Preisliste der einzelnen Unternehmen aus"""
    print('\n\n')
    for i in parcel_services:
        print(f'{i.name}')
        draw_line(90,'=')
        for j in i.parcel_options:
            print(f'|{j.name:18}',end='\t')    
        print('')    
        for j in i.parcel_options:
            if j.weight_limit ==1000:
                w_limit = 'No limit'
            else:
                w_limit = str(j.weight_limit)+'kg'
            print(f'|{w_limit:18}',end='\t')
        print('') 
        for j in i.parcel_options:
            s_limit = f'{j.size_limit}cm'
            print(f'|{s_limit:18}',end='\t')
        print('')
        for j in i.parcel_options:
            price = f'{j.price:.2f}€'
            print(f'|{price:18}',end='\t')
        print('\n')
        

def show_best_options(package):
    print(f'\n\n\nVersandoptionen für Ihr Paket \n{package.size[0]}x{package.size[1]}x{package.size[2]}cm  | {package.weight}kg')
    msg = f'\nAnbieter' + 12*' ' +'| Produkt'+13*' ' + '| Preis'
    print(msg)
    draw_line(len(msg)+1,'=')
    for i in package.best_parcel_options:
        print(f'{i.ps_name:20}| {i.name:20}| {i.price:.2f}€')

def draw_line(length = 70 ,char = '-'):
    msg = ''
    print(msg + length * char)

#Hier beginnt das Programm

#erstelle Liste von Paketdienstleister aus Dictionaries
parcel_services = []
for i in infos:
    parcel_services.append(ParcelService(i))

package = None
print('Willkommen beim Versandrechner\n')
print('Geben Sie einen Befehl oder help ein.')  
while True:
    inp = input()
    if inp == 'q':
        break

    if inp == 'help':
        show_help()

    if inp == 'new':   
        package = create_package() 
        if package == None:
            continue
        print('\n\n')
        draw_line()
        
        for i in parcel_services:
            i.add_best_option(package)
        #sortier Versandoptionen nach Preis   
        package.best_parcel_options.sort(key = lambda x: x.price)
        
        show_best_options(package)

    if inp == 'best':
        if package == None:
            print("Es fehlen Paket Eingaben.")
            continue
        show_best_options(package)

    if inp == 'prices':
        show_prices(parcel_services)

    if inp == 'about':
        draw_line()
        with open("readme.txt",encoding ='utf-8') as f:
            print(f.read())

    if inp == 'delivery':
        for i in parcel_services:
            print(f'{"".join([i.name,":"]):10}{i.calc_delivery()}')

    if inp == 'gui':
        show_gui()
        
    print('\n\n')
    draw_line()


