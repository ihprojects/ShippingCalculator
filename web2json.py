import spider_classes
import datetime
import json
import json_reader
from scrapy.crawler import CrawlerProcess

DEFAULT_TARGET_FILE= json_reader.DEFAULT_TARGET_FILE
SPIDERS =(spider_classes.HermesSpider,  #add spiders to use for crawl here
 #   spider_classes.OptionsSpider
    )   

#crwal web and save in file
def crawl(target_file=DEFAULT_TARGET_FILE):
    #add timestamp
    time = {'time': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}
    with open(target_file, 'a') as f:
        json.dump(time,f)
        f.write('\n')

    process = CrawlerProcess(settings={"FEEDS": {target_file: {"format": "jsonlines"
                ,"encoding":"utf8"},},})
    
    for i in SPIDERS:
        process.crawl(i)
        process.crawl(i)
        process.crawl(i)
    process.start()



if __name__ == '__main__':
    crawl()