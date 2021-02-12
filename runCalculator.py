import sys
import json
import PyQt5
from decimal import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
from PyQt5.QtWidgets import *
from datetime import datetime, date

from parcelServiceOption import ParcelService, ParcelOption, Parcel
from json_reader import get_newest, read_file, create_info_list
from web2json import crawl
import prices as p

SERVICES_FILE = "data.jsonl"

def get_available_services():
    '''Load available services from json file
    and initialize list of parcel_services'''
    available_services, update_at = get_newest(read_file(filename=SERVICES_FILE))
    parcel_services = []
    for service in available_services:
        parcel_services.append(ParcelService(service))
    return parcel_services

def update_services():
    '''Read service information from internet
    and fill in correct structure'''
    crawl()
    get_available_services()

def calculate():
    ''' Calculate best prices'''
    dd = w.dateEdit_delDate.date().toPyDate()
    parcel = Parcel([int(w.inp_length.text()), int(w.inp_width.text()), int(w.inp_height.text())], int(w.inp_weight.text()), dd)
    for service in parcel_services:
        service.add_best_option(parcel)          
    show_best_options(parcel)


def show_best_options(parcel):
    '''Display window with best prices for parcel'''
    while (pw.tableWidget.rowCount() > 0):
        pw.tableWidget.removeRow(0)
    selected_services = []
    if w.checkBox_dhl.isChecked():
        selected_services.append("dhl")
    
    if w.checkBox_hermes.isChecked():
        selected_services.append("hermes")
    
    if w.checkBox_dpd.isChecked():
        selected_services.append("dpd")
    
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
    r = 0
    for i in range(len(parcel.best_parcel_options)):
        option = parcel.best_parcel_options[i]
        is_required = True
        if selected_services: 
            if option.ps_name.lower() not in selected_services:   
                is_required = False
        if is_required:
            #price_formatted = str(Decimal(option.price).quantize(Decimal('.01'), rounding=ROUND_UP))
            pw.tableWidget.setItem(r,0, QTableWidgetItem(option.ps_name))
            pw.tableWidget.setItem(r,1, QTableWidgetItem(option.name))
            pw.tableWidget.setItem(r,2, QTableWidgetItem(str(option.price)))     	
            pw.tableWidget.setItem(r,3, QTableWidgetItem(option.delivery_date.strftime("%d.%m.%Y")))
            r += 1
    pw.show()    

        
def show_prices():
    '''Call window and display all services and their prices'''
    p.show_prices(parcel_services)

def close():
    w.destroy()

if __name__ == '__main__':
    parcel_services = get_available_services()
    parcel = None
    
    app = QApplication(sys.argv)                # 
    w = loadUi("vk_rechner_main.ui")            # Laden des Hauptfenster (main)
    w.but_calculate.clicked.connect(calculate)
    w.but_pricelist.clicked.connect(show_prices)
    w.but_update.clicked.connect(update_services)
    w.but_close.clicked.connect(close)
    
    # date time 
    d = QDateTime(date.today().year, date.today().month, date.today().day, 0, 0) 
    
    # setting date time 
    w.dateEdit_delDate.setDateTime(d)
    w.show()                                    # Anzeige des Fensters
    pw = loadUi("display_prices.ui")    
    sys.exit(app.exec_())                       # Applikation starten

