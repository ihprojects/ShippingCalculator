import spider_classes
import datetime
import json
from scrapy.crawler import CrawlerProcess

DEFAULT_TARGET_FILE= "data.jsonl"
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
        #process.crawl(i)
    process.start()

#read from file
def read_file(filename=DEFAULT_TARGET_FILE):
    """convert file to python dictionary"""
    with open (filename,encoding='utf8') as f:
        raw_data =list(f)
    data=[]
    for i in raw_data:
        result = json.loads(i)
        # convert timestamps
        if 'time' in result:
            result['time'] = datetime.datetime.strptime(result['time'] ,"%Y-%m-%dT%H:%M:%S")
        
        data.append(result)
    return data

#use like this: new_data ,update_from = web2json.get_newest(data)
def get_newest(data):
    idx =len(data)-1
    for i in data[::-1]:
        if 'time' in i:
            return data[idx+1:], i['time']
        idx-=1
    return data , None

def create_info_list(data):
    infos =[]
    for i in data:
        infos.append(i)
    return infos

if __name__ == '__main__':
    crawl()