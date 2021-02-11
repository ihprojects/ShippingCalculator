import json_reader 
import spider_classes
import sys
import web2json 
import parcelServiceOption
data = json_reader.read_file()
# print(type(data[0]['time'])
new_data ,update_from = json_reader.get_newest(data)
# print(new_data[0]['options'][0][1][0],type(new_data[0]['options'][0][1][0]))

# getattr(sys.modules[__name__], "Foo")


parcelservices = []
lst = json_reader.create_info_list(new_data)
for i in lst:
    parcelservices.append(parcelServiceOption.ParcelService(i))

ps =parcelservices[1]
print(ps.name)