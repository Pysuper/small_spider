import urllib
import threading
from urllib.request import Request

def main():
    for i in range(1,30):
        if i < 10:
            url = "https://dl3.diyijuzi.com/i8/uumnt/xinggan/26957/0%s.jpg" % i
        else:
            url = "https://dl3.diyijuzi.com/i8/uumnt/xinggan/26957/%s.jpg" % i
        # print(url)
        head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}

        # 使用 yield 之后,原本的函数就变成了一个可迭代的对象了
        yield url,head

def save_image(url,head):
    # TODO：获取源码的方式
    req = urllib.request.Request(url=url, headers=head)
    content = urllib.request.urlopen(req).read()

    with open("./images/%s" % url[-6:], 'wb') as f:
        f.write(content)
        print(url[-6:], "下载完成...")

if __name__ == '__main__':
    # threading.Thread(target=save_image,)
    # 可以使用多线程多进程
    for url,head in main():
        threading.Thread(target=save_image,args=(url,head)).start()


