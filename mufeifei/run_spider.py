import os
import threading
from multiprocessing.pool import Pool

from 项目实战.穆菲菲.get_person_list import get_every_page, get_every_person
from 项目实战.穆菲菲.save_images import downloads, save_img

# from .get_person_list import get_every_person
# from .save_images import downloads,save_img


url = "http://www.cct58.com/mneinv/1.html"
head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}


def get_img_href():
    img_list = []
    one_url_list = get_every_page(url)
    for href in one_url_list:
        print(href)
        person_mx27_list = get_every_person(href, head)
        img_href = downloads(person_mx27_list, head)
        img_list.append(img_href)
    return img_list


if __name__ == '__main__':

    # get_img_href()
    cpu_num = os.cpu_count()
    pool = Pool(cpu_num)
    img_src_list = get_img_href()
    for img_src in img_src_list:
        threading.Thread(target=save_img, args=(img_src, head)).start()
    pool.close()
    pool.join()
