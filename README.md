# Alphacoders-wallpaper-downloader

## 所需库

- requests
- PyQuery

## 使用方法

1. 通过 pip 等方式安装所需库
2. 将程序根目录的 `config_sample.json` 重命名为 `config.json`，将申请到的Alphacoders API Key存入文件，并可以自定义一些参数
3. 按照您的需要在 `main.py` 中调整变量 `tag_id` 和 `page` 的值
4. 执行 `main.py`

## config 说明

    {
        "api_key": "",              // 在这里填入你的 API Key
        "tag_id": "30504",          // 图片们所属的 tag_id
        "max_page": "2",            // 下载的最大页数
        "min_width": "1920"         // 图片最小宽度
    }

## 其它说明

- 比如 https://wall.alphacoders.com/tags.php?tid=30504 中的 tag_id 就是 30504