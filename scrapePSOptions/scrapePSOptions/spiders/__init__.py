# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy

#there are 5 types of spider classes in scrapy
#scrapy Spider      we use this here so our spider class must inherit from this
#Crawl Spider
#XML Feed Spider
#CSV feed spider
#sitemap spider


class OptionsSpider(scrapy.Spider):
    name = 'DHL' #use to run: scrapy crawl thisname

    start_urls = [
        'https://www.dhl.de/de/privatkunden/pakete-versenden/deutschlandweit-versenden/preise-national.html'
    ]

    def parse(self,response):
        counter =1
        # yield{response.xpath('//tbody')}
        # for option in response.xpath('(/html/body/div[4]/div[3]/div/div/div[1]/div/div[2]/table/tbody/tr)'):
        for option in response.xpath('//td[1]/p[1]/b'):
            counter = counter
            
            yield{
                
                
                # 'option_name': option.xpath('.//b').extract_first()   #use . to limit scope to option selector
               
                'option_name': option.xpath('.//text()').get()
                ,'option_limits': option.xpath(f'//tr[{counter+1}]/td[1]/p[2]/text()').get()
                ,'option_price': option.xpath(f'(//span[@class="text-primary"])[{counter}]/text()').get()
                
            }
            counter = counter
            counter +=1

        # next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        # if next_page is not None:
        #     next_page_link=response.urljoin(next_page)

        # yield scrapy.Request(url = next_page_link, callback=self.parse)

class HermesSpider(scrapy.Spider):
    name = 'Hermes' #use to run: scrapy crawl thisname
    std_girth_value = 1000

    start_urls = [
        'https://www.myhermes.de/preise/paeckchen-paket'
    ]
    #st looks like this:"Längste + kürzeste Seite bis 37 cm", " max. 25 kg", " bis 50 € Haftung\t\t\n\t</td>"
    def splitstr(self,name,st,price):
        st = st.split('<br>')[1].split(',') 
        values =[]
        values.append(name)
        for i in range(len(st)):
            newst =''
            got_value = False

            for j in range(len(st[i])):
                if st[i][j]=='k' and st[i][j+1]=='g':
                    break
                try: 
                    int(st[i][j])
                    newst+=st[i][j]
                    got_value =True
                except:
                    pass
                       
                
            if i==0 and got_value:
                values.append([int(newst)])
            elif got_value:
                values.append(float(newst)) 
            # else: 
            #     break
        newst =''
        for i in price:
            
            try: 
                int(i)
                newst+=i                 
            except:
                if i ==',':
                    newst+='.'
                else:
                    pass  

        try:
            values.append(float(newst))
        except:
            pass
        values.append(HermesSpider.std_girth_value)
        return values
        
    def parse(self,response):
        # for option in response.xpath("//div[@id ='preistabelle_2']/table/tbody/tr/td[@data-label='Paketklasse']/b"):
        lst =[]
        # for option in response.xpath("//div[@id ='preistabelle_2']/table/tr/td[@data-label='Paketklasse']"):  
        #     lst.append(option.xpath('.//b/text()').get())
        #     lst.append(self.splitstr(response.xpath("//div[@id ='preistabelle_2']/table/tr/td[@data-label='Paketklasse']").get()))
        #     lst.append(option.xpath('.//b/text()').get())


        for option in response.xpath("//div[@id ='preistabelle_2']/table/tr"):  
            # lst.append(option.xpath(".//td[@data-label='Paketklasse']/b/text()").get())
            lst.append(self.splitstr(option.xpath(".//td[@data-label='Paketklasse']/b/text()").get(),option.xpath("//div[@id ='preistabelle_2']/table/tr/td[@data-label='Paketklasse']").get(),option.xpath('.//td[3]/text()').get()))
   
        yield{
                   
                    # 'option_name': option.xpath('.//b/text()').get()   #use . to limit scope to option selector
                    # ,'option_description': self.splitstr(response.xpath("//div[@id ='preistabelle_2']/table/tr/td[@data-label='Paketklasse']").get())
                'options' : lst
                    #todo how access rwd table? maybe just ignore tbody in xpath ?  wtf google
                    # 'options': [option.xpath('.//b/text()').get(),self.splitstr(response.xpath("//div[@id ='preistabelle_2']/table/tr/td[@data-label='Paketklasse']").get())]

                # 'st':self.splitstr(response.xpath("//div[@id ='preistabelle_2']/table/tr/td[@data-label='Paketklasse']").get())
        }


        # next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        # if next_page is not None:
        #     next_page_link=response.urljoin(next_page)

        # yield scrapy.Request(url = next_page_link, callback=self.parse)

{ 'options': [
['Päckchen S', [35,25,10], 2, 3.79, 1000], ['Päckchen M',[60,30,15], 2, 4.39, 1000],
['Paket S', [60,30,15], 2, 4.99, 1000], ['Paket M', [120,60,60], 5, 5.99, 300],
['Paket L', [120,60,60], 5, 6.49, 1000], ['Paket XL', [120,60,60], 5, 6.99, 1000]],
'calc_style': 'check_sides','name': 'DHL', 'delivery_time': 3}
{ 'options': [
['Päckchen S', [35], 2, 3.79, 1000], ['Päckchen M',[60], 2, 4.39, 1000],
['Paket S', [60,30,15], 2, 4.99, 1000], ['Paket M', [120,60,60], 5, 5.99, 300],
['Paket L', [120,60,60], 5, 6.49, 1000], ['Paket XL', [120,60,60], 5, 6.99, 1000]],
'calc_style': 'sum_sides','name': 'Hermes', 'delivery_time': 3}

{"options": [
["Hermes Päckchen", [37], 25.0, 50.0, 4.5, 1000], ["S-Paket", [37], 25.0, 50.0, 5.55, 1000], ["M-Paket", [37], 25.0, 50.0, 6.85, 1000], ["L-Paket", [37], 25.0, 50.0, 11.95, 1000]
, ["XL-Paket (inkl. Abholung)", [37], 25.0, 50.0, 1000], ["XXL-Paket (inkl. Abholung)", [37], 25.0, 50.0, 1000]]