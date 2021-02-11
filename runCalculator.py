import sys
import json
import PyQt5
from decimal import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
from PyQt5.QtWidgets import *
from datetime import datetime
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
    parcel = Parcel([int(w.inp_length.text()), int(w.inp_width.text()), int(w.inp_height.text())], int(w.inp_weight.text()))
    for service in parcel_services:
        service.add_best_option(parcel)          
    show_best_options(parcel)


def show_best_options(parcel):
    pw.display_length.setText(str(parcel.sizes[0]))
    pw.display_width.setText(str(parcel.sizes[1]))
    pw.display_height.setText(str(parcel.sizes[2]))
    pw.display_weight.setText(str(parcel.weight))
    
    pw.tableWidget.setRowCount(len(parcel.best_parcel_options))                                 # Zeilenzahl = anzahl Anbieter + überschrift
    pw.tableWidget.setColumnCount(4)                              # sollten fest 4 Spalten sein

    # Überschrift (erste Zeile row0
    item = QTableWidgetItem()
    item.setText("Anbieter")
    pw.tableWidget.setHorizontalHeaderItem(0, item)
    item = QTableWidgetItem()
    item.setText("Produkt")
    pw.tableWidget.setHorizontalHeaderItem(1, item)
    item = QTableWidgetItem()
    item.setText("Preis, €")
    pw.tableWidget.setHorizontalHeaderItem(2, item)
    item = QTableWidgetItem()
    item.setText("voraussichtliches Lieferdatum")
    pw.tableWidget.setHorizontalHeaderItem(3, item)
    
    # pw.tableWidget.setItem(0,0, QTableWidgetItem("Anbieter"))
    # pw.tableWidget.setItem(0,1, QTableWidgetItem("Produkt"))
    # pw.tableWidget.setItem(0,2, QTableWidgetItem("Preis"))
    # pw.tableWidget.setItem(0,3, QTableWidgetItem("voraussichtliches Lieferdatum"))
   
    for i in range(len(parcel.best_parcel_options)):
    #for i in parcel.best_parcel_options:
        option = parcel.best_parcel_options[i]
        price_formatted = str(Decimal(option.price).quantize(Decimal('.01'), rounding=ROUND_UP))
        #print(f"{i.ps_name:20}| {i.name:20}| {price_formatted:>10} €| {i.delivery_date}")
        pw.tableWidget.setItem(i,0, QTableWidgetItem(option.ps_name))
        pw.tableWidget.setItem(i,1, QTableWidgetItem(option.name))
        pw.tableWidget.setItem(i,2, QTableWidgetItem(str(price_formatted)))
        	
        pw.tableWidget.setItem(i,3, QTableWidgetItem(option.delivery_date.strftime("%d.%m.%Y")))
    pw.show()    

        
def show_prices(parcel_service):
    print("Here open window with all available services")
    for p in parcel_services:
        print(p)

def close():
    w.destroy()

if __name__ == '__main__':
    parcel_services = get_available_services()
    parcel = None
    
    app = QApplication(sys.argv)                # 
    w = loadUi("vk_rechner_main.ui")            # Laden des Hauptfenster (main)
    w.but_calculate.clicked.connect(calculate)
    w.but_pricelist.clicked.connect(show_prices)
    w.but_close.clicked.connect(close)
    w.show()                                    # Anzeige des Fensters
    
    pw = loadUi("display_prices.ui") 
    

    sys.exit(app.exec_())                       # Applikation starten

