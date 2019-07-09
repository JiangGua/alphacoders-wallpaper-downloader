import json
import requests
from bs4 import BeautifulSoup

tag_id = 30504
page = 1

with open('api.txt', 'r') as file_obj:
    api_key = file_obj.read()

for i in range(1, page + 1):
    info = requests.get('https://wall.alphacoders.com/api2.0/get.php?auth=%s&method=tag&id=%s&page=%d&sort=views' % 
                        (api_key, tag_id, i))
    info = json.loads(info.text)

    if info['success']:
        for j in range(len(info['wallpapers'])):
            pic_info = info['wallpapers'][j]
            file_name = pic_info['id'] + '.' + pic_info['file_type']
            pic = requests.get(pic_info['url_image'])

            with open(file_name, 'wb') as file_obj:
                file_obj.write(pic.content)
        print('第 %d 页下载完成' % i)

