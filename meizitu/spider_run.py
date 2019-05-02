from mzitu_spider.get_info import main
from mzitu_spider.downloads import images_downloads


if __name__ == '__main__':
    url = "http://www.mzitu.com"
    file_name = input("\n文件较多,先选一手保存目录:")

    for group_href, group_title, menu_name in main(url, file_name):
        images_downloads(group_href, file_name, menu_name)
