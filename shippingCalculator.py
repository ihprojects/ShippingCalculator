import json
from decimal import *
from datetime import date, timedelta
import parcelServiceOption
from parcelServiceOption import ParcelService, ParcelOption, Parcel
from json_reader import get_newest, read_file, create_info_list

SERVICES_FILE = "data.jsonl"
TEST_FILE = "services.json"
     
def create_parcel():
    """Erstellt ein neues Paket nach Eingaben"""
    print('Bitte geben Sie die Paketmaße in cm ein')
    L = int(input('Länge: '))
    W = int(input('Breite: '))
    H = int(input('Höhe: '))
    weight = int(input('Gewicht in kg: '))  
    return Parcel([L,W,H], weight)

def show_help():
    print('\nSie können die folgenden Befehle verwenden:\n')
    commands={'q': 'verlässt das Programm'
        ,'about' : 'Informationen über dieses Programm'
        ,'new' : create_parcel.__doc__
        ,'prices' : print_prices.__doc__
        ,'best' : 'zeigt die günstigsten Versandoptionen'
        }
    for i in commands.items():
        print(f'{i[0] :20}\t{i[1]}')
        
def find_best_optios(parcel_services, parcel):
    for i in parcel_services:
        i.add_best_option(parcel)  
    
def print_prices(parcel_service):
    """Gibt die Preisliste der einzelnen Unternehmen aus"""
    print('\n\n')
    print(f'{parcel_service.name}')
    draw_line(90,'=')
    for j in parcel_service.parcel_options:
        print(f'|{j.name:18}',end='\t')    
    print('')    
    for j in parcel_service.parcel_options:
        if j.weight_limit ==1000:
            w_limit = 'No limit'
        else:
            w_limit = str(j.weight_limit)+'kg'
        print(f'|{w_limit:18}',end='\t')
    print('') 
    for j in parcel_service.parcel_options:
        s_limit = f'{j.size_limit}cm'
        print(f'|{s_limit:18}',end='\t')
    print('')
    for j in parcel_service.parcel_options:
        price = f'{j.price:.2f}€'
        print(f'|{price:18}',end='\t')
    print('\n')
        

def show_best_options(parcel):
    print(f'\n\n\nVersandoptionen für Ihr Paket \n{parcel.sizes[0]}x{parcel.sizes[1]}x{parcel.sizes[2]}cm  | {parcel.weight}kg')
    msg = f'\nAnbieter' + 12*' ' +'| Produkt'+13*' ' + '| Preis'+7*' ' + '| Expected delivery'
    print(msg)
    draw_line(len(msg)+1,'=')
    for i in parcel.best_parcel_options:
        price_formatted = str(Decimal(i.price).quantize(Decimal('.01'), rounding=ROUND_UP))        
        print(f"{i.ps_name:20}| {i.name:20}| {price_formatted:>10} €| {i.delivery_date}")

def draw_line(length = 70 ,char = '-'):
    msg = ''
    print(msg + length * char)

def get_available_services():
    '''Load available services from json file
    and initialize list of parcel_services'''
    available_services, update_at = get_newest(read_file(filename=SERVICES_FILE))
    parcel_services = []
    for service in available_services:
        parcel_services.append(ParcelService(service))
    return parcel_services

def get_available_services_test():
    '''Load available services from json file
    and initialize list of parcel_services'''
    available_services = []   
    with open(TEST_FILE, encoding='utf-8') as f:
        available_services = json.load(f)
    parcel_services = []
    for service in available_services:
        parcel_services.append(ParcelService(service))
    return parcel_services
        
def get_price_services():
    return get_available_services()

#Hier beginnt das Programm
if __name__ == '__main__':
    parcel_services = get_available_services()
    parcel = None
    print('Willkommen beim Versandrechner\n')
    print('Geben Sie einen Befehl oder help ein.')  
    while True:
        inp = input()
        if inp == 'q':
            break
                
        if inp == 'help':
            show_help()

        if inp == 'new': 
            parcel = create_parcel()
            if parcel == None:
                continue
            print('\n\n')
            draw_line()
            find_best_optios(parcel_services, parcel)          
            show_best_options(parcel)

        if inp == 'best':
            if parcel == None:
                print("Es fehlen Paket Eingaben.")
                continue
            show_best_options(parcel)

        if inp == 'prices':
            for ps in parcel_services:
                print_prices(ps)

        if inp == 'about':
            draw_line()
            with open("readme.txt",encoding ='utf-8') as f:
                print(f.read())
                
        print('\n\n')
        draw_line()


