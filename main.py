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

print(config)

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

