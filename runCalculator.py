import sys
import json

from decimal import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
from PyQt5.QtWidgets import *
from parcelServiceOption import ParcelService, ParcelOption, Parcel

SERVICES_FILE = "services.json"

def get_available_services():
    '''Load available services from json file
    and initialize list of parcel_services'''
    available_services = []   
    with open(SERVICES_FILE, encoding='utf-8') as f:
        available_services = json.load(f)
    parcel_services = []
    for service in available_services:
        parcel_services.append(ParcelService(service))
    return parcel_services

def calculate():
    #TODO convert to int in nicer way
    parcel = Parcel([int(w.inp_length.text()), int(w.inp_width.text()), int(w.inp_height.text())], int(w.inp_weight.text()))
    for service in parcel_services:
        service.add_best_option(parcel)          
    show_best_options(parcel)

def show_best_options(parcel):
    for i in parcel.best_parcel_options:
        price_formatted = str(Decimal(i.price).quantize(Decimal('.01'), rounding=ROUND_UP))
        # TODO send to vk_rechner_main      
        print(f"{i.ps_name:20}| {i.name:20}| {price_formatted:>10} €| {i.delivery_date}")
        
def show_prices(parcel_service):
    print("Here open window with all available services")
    for p in parcel_services:
        print(p)

def alternate():
    print("TODO")

def close():
    w.destroy()
    
def show_help_w():
    print("TODO")

if __name__ == '__main__':
    parcel_services = get_available_services()
    parcel = None
    
    app = QApplication(sys.argv)                # 
    w = loadUi("vk_rechner_main.ui")            # Laden des Hauptfenster (main)
    w.but_calculate.clicked.connect(calculate)
    w.but_pricelist.clicked.connect(show_prices)
    w.but_alternate.clicked.connect(alternate)
    w.but_close.clicked.connect(show_help_w)
    w.but_close.clicked.connect(close)
    w.show()                                    # Anzeige des Fensters

    sys.exit(app.exec_())                       # Applikation starten

