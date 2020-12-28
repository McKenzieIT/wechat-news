import requests
import threading
import random
import logging

class UserAgent(object):
    _instance_lock = threading.Lock()
    
    def __init__(self):
        self.__agents_pool = list()
        with open('./UserAgents/useragents.txt','r') as read_ob:
            for line in read_ob.readlines():
                self.__agents_pool.append(line.strip())
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(UserAgent, "_instance"):
            with UserAgent._instance_lock:
                if not hasattr(UserAgent, "_instance"): 
                    UserAgent._instance = object.__new__(cls)
        return UserAgent._instance
    
    def get_useragent_randomly(self):
        return random.choice(self.__agents_pool)
    

class Crawl():

    def __init__(self):
        self.__session = None
        self.__headers = {
            'User-Agent': UserAgent().get_useragent_randomly(),
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-cn',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
        }
        
    def request_get(self, url, **kwargs):
        logging.info('scraping {}...'.format(url))
        try:
            response = requests.get(url, headers=self.__headers,**kwargs)
            if response.status_code == 200:
                return response
            logging.error('get invalid status code %s while scraping %s', response.status_code, self.__url)
        except requests.RequestException:
            logging.error('error occurred while scraping %s', url, exc_info=True)
        else:
            logging.info('scraping {} finished'.format(url))
     
    def request_post(self, url, **kwargs):
        logging.info('scraping {}...'.format(url))
        try:
            response = requests.post(url, headers=self.__headers,**kwargs)
            if response.status_code == 200:
                return response
            logging.error('get invalid status code %s while scraping %s', response.status_code, self.__url)
        except requests.RequestException:
            logging.error('error occurred while scraping %s', url, exc_info=True)
        else:
            logging.info('scraping {} finished'.format(url))
    
    def session_get(self, url, **kwargs):
        self.check_session()
        logging.info('scraping {}...'.format(url))
        try:
            response = self.__session.get(url, headers=self.__headers,**kwargs)
            if response.status_code == 200:
                return response
            logging.error('get invalid status code %s while scraping %s', response.status_code, self.__url)
        except requests.RequestException:
            logging.error('error occurred while scraping %s', url, exc_info=True)
        else:
            logging.info('scraping {} finished'.format(url))
    
    def session_post(self, url, **kwargs):
        self.check_session()
        logging.info('scraping {}...'.format(url))
        try:
            response = self.__session.post(url, headers=self.__headers,**kwargs)
            if response.status_code == 200:
                return response
            logging.error('get invalid status code %s while scraping %s', response.status_code, self.__url)
        except requests.RequestException:
            logging.error('error occurred while scraping %s', url, exc_info=True)
        else:
            logging.info('scraping {} finished'.format(url))        
    def check_session(self):
        if self.__session == None:
            self.__session = requests.session()
        return
    
    def add_header(self, headers):
        for key, value in headers.items():
            self.__headers[key] = value
