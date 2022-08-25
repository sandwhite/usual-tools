import urllib.request
import gevent
from gevent import monkey

monkey.patch_all()


def downloader(img_name, img_url):
    req = urllib.request.urlopen(img_url)
    img_content = req.read()

    with open(img_name, "wb") as f:
        f.write(img_content)

def main():
    gevent.joinall([
        gevent.spawn(downloader, "3.png", "https://rpic.douyucdn.cn/live-cover/appCovers/2020/03/29/8426594_20200329100914_small.jpg")
    ])


if __name__ == main():
    main()
