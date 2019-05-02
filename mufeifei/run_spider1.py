import os
import threading
import time
from multiprocessing.pool import Pool

from 项目实战.穆菲菲.get_person_list1 import get_every_page, get_every_person
from 项目实战.穆菲菲.save_images1 import downloads, save_img

# from .get_person_list import get_every_person
# from .save_images import downloads,save_img


url = "http://www.cct58.com/mneinv/1.html"
head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}


def get_img_href():
    save_path = input("文件保存在:")
    one_url_list = get_every_page(url)
    # for href in one_url_list:
    #     person_mx27_list,title = get_every_person(href, head)
    #     # downloads(person_mx27_list, head,save_path,title)
    os.cpu_count()
    pool = Pool(os.cpu_count())
    for href in one_url_list:
        try:
            person_mx27_list,title_list = get_every_person(href, head)
            # print(person_mx27_list,title_list)
            # threading.Thread(target=downloads,args=(person_mx27_list, head,save_path,title))
            pool.apply_async(downloads,args=(person_mx27_list, head,save_path,title_list))
            time.sleep(1)
        except:
            continue
    pool.close()
    pool.join()

if __name__ == '__main__':
    get_img_href()