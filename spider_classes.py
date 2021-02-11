# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import sys

#there are 5 types of spider classes in scrapy
#scrapy Spider      we use this here so our spider class must inherit from this
#Crawl Spider
#XML Feed Spider
#CSV feed spider
#sitemap spider


class DHLSpider(scrapy.Spider):
    name = 'DHL' #use to run: scrapy crawl thisname

    start_urls = [
        'https://www.dhl.de/de/privatkunden/pakete-versenden/deutschlandweit-versenden/preise-national.html'
    ]
    DEFAULT_DELIVERY_TIME =2
    DEFAULT_GIRTH_VALUE = 1000

    def update_dhl(self,name_gewicht, dimensionen, preis):
       
        asd = []
        
        gewichts = name_gewicht
        klassenname = [g2 for g2 in gewichts.replace(',','.').split()]
        kln = f'{klassenname[0]} {klassenname[1]} {klassenname[2]} {klassenname[3]}'
        asd.append(kln)

        limits = dimensionen
        dim1 = [int(d) for d in limits.split() if d.isdigit()] 
        asd.append(dim1)

        gewicht1 = [g for g in gewichts.replace(',','.').split() if g.isdigit]
        for g1 in gewicht1:
            if g1.isdigit():
                g1 = int(g1)
            else:
                g1 = float(gewicht1[-2]) 
        asd.append(g1)
    
        prs = preis
        prs1 = [p for p in prs.replace(',','.').split()]
        p1 = float(prs1[0])
        asd.append(p1)
        asd.append(DHLSpider.DEFAULT_GIRTH_VALUE)
            
        return asd



    def parse(self,response):
            
        lst1 =[]
        counter =1
    #path in browser might be different as som browser add /tbody in xpath
        for option in response.xpath('//td[1]/p[1]/b'):  
            lst1.append(self.update_dhl(option.xpath('.//text()').get(), option.xpath(f'//tr[{counter+1}]/td[1]/p[2]/text()').get(), option.xpath(f'(//span[@class="text-primary"])[{counter}]/text()').get()))
            counter+=1
        yield{
                'update' : DHLSpider.name
                ,'options' : lst1
                ,'calc_style': 'check_sides'
                ,'name': 'DHL'
                ,'delivery_time': DHLSpider.DEFAULT_DELIVERY_TIME
                    
    
            }


class HermesSpider(scrapy.Spider):
    name = 'Hermes' #use to run: scrapy crawl thisname
    DEFAULT_GIRTH_VALUE = 1000
    DEFAULT_MAX_3rd_SIDE_LIMIT = 1000
    DEFAULT_DELIVERY_TIME = 3
    
    
    start_urls = [
        'https://www.myhermes.de/preise/paeckchen-paket'
    ]
#each of the given parameters is some text from website
    def splitstr(self,name,st,price):
        values = []

#name needs no parsing
        values.append(name)
                
        st_list = st.split('<br>')[1].split('kg')[0].split('cm')
        #st now looks like one of these:
        #["Längste + kürzeste Seite 120,1 bis 150 ", ", max. 31,5 "]
        # ["Längste + kürzeste te 150,1Sei bis 200 ", ", dritte Seite max. 50 ", ", max. 31,5 "]
        val1 = 0
        val2 = HermesSpider.DEFAULT_MAX_3rd_SIDE_LIMIT
        

#get size limit
        newst =''
        for i in st_list[0].split('bis')[-1]:
            try:
                int(i)
                newst+=i
            except:
                pass
        if len(newst)>0:
            val1 =int(newst)
#check if middle part exists i.e.(", dritte Seite max. 50 ")
        if len(st_list)>2:
            newst=''
            for i in st_list[1]:
                try:
                    int(i)
                    newst+=i
                except:
                    pass
            if len(newst)>0:
                val2 =int(newst)

        values.append([val1,val2])
#get max weight
        newst = ''
        got_value =False    
 
        for i in st_list[-1]:
            try:
                int(i)
                newst+=i
                got_value =True
            except:
                 if i ==',' and got_value==True:
                     newst+='.'
        if len(newst)>0:
            values.append(float(newst))

#get price
        newst =''
        for i in price:        
            try: 
                int(i)
                newst+=i                 
            except:
                if i ==',':
                    newst+='.'

        try:
            values.append(float(newst))
        except:
            values.append('price not found')
        values.append(HermesSpider.DEFAULT_GIRTH_VALUE)
        return values


#gets called by default
    def parse(self,response):
        
        lst =[]

#path in browser might be different as som browser add /tbody in xpath
        for option in response.xpath("//div[@id ='preistabelle_2']/table/tr"):  
            lst.append(self.splitstr(option.xpath(".//td[@data-label='Paketklasse']/b/text()").get()
            , option.xpath(".//td[@data-label='Paketklasse']").get()
            ,option.xpath('.//td[4]/a/text()').get()))
        yield{

                'update' : HermesSpider.name
                ,'options' : lst
                ,'calc_style': "check_sum"
                ,'name': 'Hermes'
                ,'delivery_time': HermesSpider.DEFAULT_DELIVERY_TIME
                
        }
