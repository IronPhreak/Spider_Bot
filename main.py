import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *


class crawler():
    PROJECT_NAME = ''
    HOMEPAGE = ''
    DOMAIN_NAME = get_domain_name(HOMEPAGE)
    QUEUE_FILE = ''
    CRAWLED_FILE = ''
    NUMBER_OF_THREADS = 8
    queue = Queue()

    @staticmethod
    def work():
        while True:
            url = crawler.queue.get()
            Spider.crawl_page(threading.current_thread().name, url)
            crawler.queue.task_done()

    @staticmethod
    def create_workers():
        for _ in range(crawler.NUMBER_OF_THREADS):
            t = threading.Thread(target=crawler.work)
            t.daemon = True
            t.start()


    @staticmethod
    def crawl():
        queued_linked = file_to_set(crawler.QUEUE_FILE)
        if len(queued_linked) > 0:
            print(str(len(queued_linked)) + " links in the queue")
            crawler.create_jobs()

    @staticmethod
    def create_jobs():
        for link in file_to_set(crawler.QUEUE_FILE):
            crawler.queue.put(link)
        crawler.queue.join()
        crawler.crawl()

    @staticmethod
    def setup_project():
        crawler.PROJECT_NAME = input("What is the name of your project?: ")
        crawler.HOMEPAGE = input("What is your homepage?: ")
        crawler.QUEUE_FILE = crawler.PROJECT_NAME + "/queue.txt"
        crawler.CRAWLED_FILE = crawler.PROJECT_NAME + "/crawled.txt"
        Spider(crawler.PROJECT_NAME, crawler.HOMEPAGE, crawler.DOMAIN_NAME)


crawler.setup_project()
crawler.create_workers()
crawler.crawl()