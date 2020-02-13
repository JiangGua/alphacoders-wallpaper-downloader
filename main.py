import os
import time
import json
import requests
from pyquery import PyQuery as pq
from threading import Thread

def download_pic(url, name):
    pic = requests.get(url)
    with open(name, 'wb') as file_obj:
        file_obj.write(pic.content)

def fetch(api_key, tag_id, min_width, i):
    info = requests.get('https://wall.alphacoders.com/api2.0/get.php?auth=%s&method=tag&id=%s&page=%d&sort=views' % 
                        (api_key, tag_id, i))
    info = json.loads(info.text)

    if info['success']:
        if len(info['wallpapers']) == 0:
            print('开始下载…')
            return False

        result = []

        for j in range(len(info['wallpapers'])):
            pic_info = info['wallpapers'][j]

            # 若当前图片小于设定的min_width，则直接下一张
            if int(pic_info['width']) < min_width:
                continue

            file_name = pic_info['id'] + '.' + pic_info['file_type']
            if os.path.exists(file_name):
                continue

            result.append({
                "url": pic_info['url_image'],
                "name": file_name,
            })
            

        print('已将第 %d 页添加到下载队列' % i)
        return result

if __name__ == "__main__":
    # Read Config
    with open('config.json', 'r') as file_obj:
        config = file_obj.read()
        config = json.loads(config)
        tag_id = str(config['tag_id'])
        api_key = str(config['api_key'])
        try:
            max_page = int(config['max_page'])
        except:
            max_page = 0
        try:
            min_width = int(config['min_width'])
        except:
            min_width = 0

    # Main
    url = 'https://wall.alphacoders.com/tags.php?tid=' + str(tag_id)
    html = pq(url=url)
    dir_name = html('span.breadcrumb-element').text()
    dir_name = "".join(i for i in dir_name if i.isalnum())
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    os.chdir(dir_name)

    queue = []  # 下载链接和对应图片文件名的全列表(下载队列)
    threads = []

    if max_page != 0:
        for i in range(1, max_page + 1):
            result = fetch(api_key, tag_id, min_width, i)
            if result == False:
                break
            queue += result
    else:
        i = 1
        while True:
            result = fetch(api_key, tag_id, min_width, i)
            if result == False:
                break
            queue += result
            i += 1

    for i in queue:
        t = Thread(target = download_pic, args = [i["url"], i["name"]])
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

    print("下载完成")