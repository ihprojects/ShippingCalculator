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
            