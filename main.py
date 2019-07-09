import os
import json
import requests
from bs4 import BeautifulSoup

with open('config.json', 'r') as file_obj:
    config = file_obj.read()
    config = json.loads(config)
    tag_id = str(config['tag_id'])
    max_page = int(config['max_page'])
    api_key = str(config['api_key'])
    min_width = int(config['min_width'])

info = requests.get('https://wall.alphacoders.com/api2.0/get.php?auth=%s&method=tag&id=%s&page=1&sort=views&info_level=3' %
                    (api_key, tag_id))
info = json.loads(info.text)
dir_name = info['wallpapers'][0]['sub_category']
dir_name = "".join(i for i in dir_name if i.isalnum())
if not os.path.isdir(dir_name):
    os.mkdir(dir_name)
os.chdir(dir_name)

for i in range(1, max_page + 1):
    info = requests.get('https://wall.alphacoders.com/api2.0/get.php?auth=%s&method=tag&id=%s&page=%d&sort=views' % 
                        (api_key, tag_id, i))
    info = json.loads(info.text)

    if info['success']:
        for j in range(len(info['wallpapers'])):
            pic_info = info['wallpapers'][j]

            # 若当前图片小于设定的min_width，则直接下一张
            if int(pic_info['width']) < min_width:
                continue

            file_name = pic_info['id'] + '.' + pic_info['file_type']
            pic = requests.get(pic_info['url_image'])

            with open(file_name, 'wb') as file_obj:
                file_obj.write(pic.content)
        print('第 %d 页下载完成' % i)

