from datetime import date, timedelta

#Ein Paket
class Parcel():
    '''Describes parcel'''
    def __init__(self, sizes, weight, send_day = date.today()):
        '''Instantiate parcel
        sizes[0] - longest, sizes[1] - middle, sizes[2] - shortest side'''
        self.sizes = sorted(sizes,reverse=True)
        self.weight = weight
        self.send_day = send_day
        self.best_parcel_options = []
    
    # Gurtmaß    
    def get_girth(self):
        '''Delivers combined length and girth'''
        return (self.sizes[0] + 2*self.sizes[1] + 2*self.sizes[2])

#Versandoptionen z.B. "Paket M"
class ParcelOption():
    '''Parcel sending option'''
    def __init__(self, ps_name, name, size_limit, weight_limit, price, girth):
        self.ps_name = ps_name
        self.name = name
        self.size_limit = size_limit
        self.weight_limit = weight_limit
        self.price = price
        self.girth = girth

#Versanddienstleister
class ParcelService():
    '''Parcel delivery service'''
    
    def __init__(self, info):
        '''Instantiate parcel service'''
        self.name = info['name']
        self.parcel_options = self.create_parcel_options(info['name'],info['options'])
        self.calc_type = info['calc_style']
        self.ship_duration = info['delivery_time']
        self.delivery_date = None

    def create_parcel_options(self, ps_name, options):
        '''Creates parcel send options, here
        options[0] - option name
        options[1] - size information
        options[2] - weight information
        options[3] - price information
        options[4] - girth limit information'''           
        parcel_options = []
        for option in options:
            parcel_options.append(ParcelOption(ps_name, option[0], option[1], option[2], option[3], option[4]))
        return parcel_options
        
    def add_best_option(self,parcel):      
        #teste ob wir versanoptionen für unser Paket nutzen können
        for option in self.parcel_options:
            lowest_price = 100000
            best_parcel_option = None
            is_valid = False
            if self.calc_type == "check_sides": 
                if (parcel.sizes <= option.size_limit and 
                    parcel.weight <= option.weight_limit and 
                    parcel.get_girth() <= option.girth):
                    is_valid = True    
                               
            if self.calc_type == "check_sum":            
                if ((parcel.sizes[0] + parcel.sizes[2]) <= option.size_limit[0] and 
                    parcel.weight <= option.weight_limit and 
                    parcel.get_girth() <= option.girth):
                    is_valid = True                
            
            #check if lowest price
            if is_valid:
                if option.price < lowest_price:
                    lowest_price = option.price
                    best_parcel_option = option

        if best_parcel_option != None:
            best_parcel_option.delivery_date = self.calc_delivery(parcel.send_day)
            parcel.best_parcel_options.append(best_parcel_option) 
        
        # Price options are always sorted    
        parcel.best_parcel_options.sort(key = lambda x: x.price) 
    
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