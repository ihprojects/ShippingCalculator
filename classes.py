from datetime import date, timedelta

#Ein Paket
class Package():
    def __init__(self,size,weight):
        self.size = size
        self.weight = weight
        self.best_parcel_options = []

#Versandoptionen z.B. "Paket M"
class ParcelOption():
    def __init__(self, name, size_limit, weight_limit, price,ps_name, girth = False):
        self.name = name
        self.size_limit = size_limit
        self.weight_limit = weight_limit
        self.price = price
        self.ps_name = ps_name
        self.girth = girth

#Versanddienstleister
class ParcelService():
    def __init__(self, info):
        self.name = info['name']
        self.parcel_options = self.create_parcel_options(info['options'])
        self.calc_type = info['calc_style']
        self.ship_duration = info['delivery_time']

    def create_parcel_options(self,options):
        parcel_options = []
        for i in options.keys():
            girth = False
            if options[i][3] != 'n':
                girth == True
            parcel_options.append(ParcelOption(i, options[i][0], options[i][1], options[i][2], self.name ,girth))
        return parcel_options
    
    def show_parcel_options(self):
        for i in self.parcel_options:
            print(f'{i.name:20} max Maße: {str(i.size_limit):20}max Gewicht: {i.weight_limit:5} kg \tPreis: {i.price:.2f}')


    def add_best_option(self,package):
        lowest_price = 100000
        best_parcel_option = None
        
        #teste ob wir versanoptionen für unser Paket nutzen können
        for i in self.parcel_options:
            is_valid = False
            valid_found = 0
            if self.calc_type == 1: 
                for j in range(0,len(i.size_limit)):
                    if i.size_limit[j] >= package.size[j] and i.weight_limit >= package.weight:
                        valid_found += 1 
                is_valid = (valid_found == len(i.size_limit))    
            if self.calc_type == 2:            
                if i.size_limit[0] >= package.size[0]+package.size[2] and i.weight_limit >= package.weight:
                    is_valid = True                
            
            #check if lowest price
            if is_valid:
                if i.price < lowest_price:
                    lowest_price = i.price
                    best_parcel_option = i

        if best_parcel_option != None:
            package.best_parcel_options.append(best_parcel_option)  
    
    #ermittle voraussichtliches Lieferdatum
    def calc_delivery(self, send_day = date.today()):
        """ Calculate delivery depending on duration, exlude Sunday"""
        delivery_day = send_day
        added_days = 0
        while added_days < self.ship_duration:
            delivery_day += timedelta(days=1)
            if delivery_day.weekday() == 6: # is Sunday
                continue
            added_days += 1
        return delivery_day