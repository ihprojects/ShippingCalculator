import json
import datetime
DEFAULT_TARGET_FILE= "data.jsonl"



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