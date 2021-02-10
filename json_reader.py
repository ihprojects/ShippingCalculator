import json 
import datetime

with open ('data.jsonl',encoding='utf8') as f:
    raw_data =list(f)


def get_newest_data(raw_data):
    idx =len(raw_data)-1
    for i in raw_data[::-1]:
        result = json.loads(i)
        if 'time' in result:
            return idx+1, datetime.datetime.strptime(result['time']
            ,"%Y-%m-%dT%H:%M:%S")
        idx-=1
    return 0 , None
def create_info_list(raw_data):
    infos =[]
    for i in raw_data:

        infos.append(json.loads(i))
    return infos


idx ,last_update= get_newest_data(raw_data)
infos = create_info_list(raw_data[idx:])
print(infos[0]['options'][0][1][0],type(infos[0]['options'][0][1][0]))
