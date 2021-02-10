import spider_classes
import datetime
import json
from scrapy.crawler import CrawlerProcess

target_file= "data.jsonl"

#add timestamp
time = {'time': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}
with open(target_file, 'a') as f:
    json.dump(time,f)
    f.write('\n')

process = CrawlerProcess(settings={
    "FEEDS": {
        target_file: {
            "format": "jsonlines"
            ,"encoding":"utf8"
        },
    },
})
# process.crawl(sp.OptionsSpider)
process.crawl(spider_classes.HermesSpider)
process.crawl(spider_classes.HermesSpider)
process.start()