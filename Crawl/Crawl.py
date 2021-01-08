import logging
import random
import re
import threading
from queue import Queue

import requests


class UserAgent():
    __instance_lock = threading.Lock()
    __init_flag = False
    
    def __init__(self):
        if self.__init_flag is False:
            print('init UserAgent')
            self.__agents_pool = list()
            with open('Crawl/UserAgents/useragents.txt','r') as read_ob:
                for line in read_ob.readlines():
                    self.__agents_pool.append(line.strip())
            self.__init_flag = True
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(UserAgent, "_instance"):
            print('new UserAgent')
            with UserAgent.__instance_lock:
                if not hasattr(UserAgent, "_instance"): 
                    UserAgent._instance = object.__new__(cls)
        return UserAgent._instance
    
    def get_useragent_randomly(self):
        return random.choice(self.__agents_pool)
    

class Crawl():

    def __init__(self):
        self._session = None
        self._headers = {
            'User-Agent':UserAgent().get_useragent_randomly(),
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-cn',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
        }
        self._proxies = [
            {"http":"59.35.71.49:4230"},
            {"http":"59.34.123.123:4287"},
            {"http":"183.7.136.6:4230"},
            {"http":"27.44.214.135:4265"},
            {"http":"113.110.52.241:4245"}
        ]
        
    def request_get(self, url, **kwargs):
        logging.info('scraping {}...'.format(url))
        try:
            response = requests.get(url, headers=self._headers, proxies=random.choice(self._proxies), **kwargs)
            if response.status_code == 200:
                return response
            logging.error('get invalid status code %s while scraping %s', response.status_code, url)
        except requests.RequestException:
            logging.error('error occurred while scraping %s', url, exc_info=True)
        else:
            logging.info('scraping {} finished'.format(url))
     
    def request_post(self, url, **kwargs):
        logging.info('scraping {}...'.format(url))
        try:
            response = requests.post(url, headers=self._headers, proxies=random.choice(self._proxies), **kwargs)
            if response.status_code == 200:
                return response
            logging.error('get invalid status code %s while scraping %s', response.status_code, url)
        except requests.RequestException:
            logging.error('error occurred while scraping %s', url, exc_info=True)
        else:
            logging.info('scraping {} finished'.format(url))
    
    def session_get(self, url, **kwargs):
        self.check_session()
        logging.info('scraping {}...'.format(url))
        try:
            response = self._session.get(url, headers=self._headers, proxies=random.choice(self._proxies), **kwargs)
            if response.status_code == 200:
                return response
            logging.error('get invalid status code %s while scraping %s', response.status_code, url)
        except requests.RequestException:
            logging.error('error occurred while scraping %s', url, exc_info=True)
        else:
            logging.info('scraping {} finished'.format(url))
    
    def session_post(self, url, **kwargs):
        self.check_session()
        logging.info('scraping {}...'.format(url))
        try:
            response = self._session.post(url, headers=self._headers, proxies=random.choice(self._proxies), **kwargs)
            if response.status_code == 200:
                return response
            logging.error('get invalid status code %s while scraping %s', response.status_code, url)
        except requests.RequestException:
            logging.error('error occurred while scraping %s', url, exc_info=True)
        else:
            logging.info('scraping {} finished'.format(url)) 

    def get_session(self):
        return self._session
    
    def set_session(self, session):
        self._session = session
        return True

    def get_cookies(self):
        if self._session is not None:
            return self._session.cookies
        else:
            return False
    
    def set_cookies(self, cookies):
        if self._session is not None:
            self._session.cookies = cookies
            return True
        else:
            return False
    
    def save_cookies(self, response):
        cookieJar = requests.cookies.RequestsCookieJar()
        for cookie in response.cookies:
            cookieJar.set(cookie.name,cookie.value)
        for cookie in response.headers['Set-Cookie'].split(";"):
            key = cookie.split('=')[0]
            value = cookie.split('=')[1]
            cookieJar.set(key,value)
        self.set_cookies(cookieJar)
        return cookieJar
    
    def check_session(self):
        if self._session == None:
            self._session = requests.session()
        return
    
    def add_header(self, headers):
        for key, value in headers.items():
            self._headers[key] = value
