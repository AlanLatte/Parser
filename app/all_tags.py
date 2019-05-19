from flask       import current_app as app
from app.parser  import get_data as parser
from json        import load
import os

def all_tags(file_name='DATA_OF_ALL_TAGS', FILE_OF_TAGS='TAGS'):
    with open(os.path.join(app.config['ALL_TAGS'], f'{FILE_OF_TAGS}.json'), mode='r', encoding='utf8') as json_file:
        data = load(json_file)
    long_data        = str()
    file_name        =   'DATA_OF_ALL_TAGS'
    for item in data.keys():
        direction = data[item].keys()
        for sub_item in direction:
            long_data += f'------{sub_item}------\n'
            for sub_sub_item in data[item][sub_item]:
                long_data+= f'------NAME: {sub_sub_item["name"]}------\n'
                long_data+= f'------CODE: {sub_sub_item["code"]}------\n'
                tags      = sub_sub_item["tags"]
                long_data+= f'------TAGS: {        tags        }------\n\n'
                long_data+= parser  (
                                        search_data =   tags,
                                        name        =   file_name,
                                        get_all_tags=   True
                                    )
    with open(os.path.join(app.config['DATA_BASE_STORAGE'], f'{file_name}.txt'), mode='w', encoding='utf8') as outfile:
        outfile.write(long_data)
