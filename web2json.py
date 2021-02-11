import spider_classes
import datetime
import json
import json_reader as jr
from scrapy.crawler import CrawlerProcess

DEFAULT_TARGET_FILE= jr.DEFAULT_TARGET_FILE
SPIDERS ={  #add spiders to use for crawl here
    spider_classes.DHLSpider.name : spider_classes.DHLSpider
    ,spider_classes.HermesSpider.name : spider_classes.HermesSpider
    }  

#crwal web and save in file
def crawl(target_file=DEFAULT_TARGET_FILE,init = False):

    process = CrawlerProcess(settings={"FEEDS": {target_file: {"format": "jsonlines"
                ,"encoding":"utf8"},},})


    data =jr.get_newest(jr.read_file(DEFAULT_TARGET_FILE))[0]
    copied_entries =[]
    if init == False:
        for i in data:
            if(i['update'] in SPIDERS):
                process.crawl(SPIDERS[i['update']])
            else:
                copied_entries.append(i)
    else:
        for i in SPIDERS:
            print(i)
            process.crawl(SPIDERS[i])
            

    #add timestamp
    if init == False:
        time = {'time': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}
        with open(target_file, 'a') as f:
            json.dump(time,f)
            f.write('\n')

       
    process.start()

    if copied_entries:
        for i in copied_entries:
            with open(target_file, 'a') as f:
                json.dump(i,f)
                f.write('\n')


if __name__ == '__main__':
    crawl(init = False)
