from Crawl import Crawl
from utils import run_time

class DoubanUser(Crawl):
    __instance_lock = threading.Lock()
    __init_flag = False
       
    def __init__(self):
        if self.__init_flag is False:
            super(DoubanUser, self).__init__()
            self.__user = None
    #         self._cookies = None
            self.__login()
            self.__init_flag = True

    def __new__(cls, *args, **kwargs):
        if not hasattr(DoubanUser, "_instance"):
            print('new Douban')
            with DoubanUser.__instance_lock:
                if not hasattr(Douban, "_instance"): 
                    DoubanUser._instance = object.__new__(cls)
        return DoubanUser._instance
    
    def __login(self):
        post_data = {
            'name':'18664678368',
            'password':'Ljc970412',
            'remember':'false'
        }
        self.add_header({
            "Referer":'https://accounts.douban.com/passport/login'
        })
        user = self.session_post('https://accounts.douban.com/j/mobile/login/basic', data=post_data)
        login_detail = json.loads(user.text)
        if login_detail['status'] == 'success':
            print('login success!')
            self.__user =  user.text
#             self.__cookies = self.save_cookies(user)
        else:
            print('login failed!')
    
    def get_user_info(self):
        return self.__user

class Douban(Crawl):
    
    def __init__(self, douban_user):
        super(Douban, self).__init__()
        self.set_session(douban_user.get_session())
    
    def search(self, query, cat=''):
        res = dict()
        params = {
            'q':query,
            'cat':cat
        }
        count=0
        response = self.session_get('https://www.douban.com/search', params=params)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find(class_='result-list').find_all(class_='result')
        for result in results:
            pic = result.find(class_='pic')
            content = result.find(class_='content')
            img = pic.img.get('src')
            link = content.a.get('href')
            name = content.a.text
            description = content.p.text if content.p else ''
            res[count]={
                'name':name,
                'img':img,
                'link':link,
                'description':description
            }
            count+=1
        return res

class DoubanMovie(Douban):
    
    @run_time
    def get_comments(self, **kwargs):
        
        count = 0
        queue = Queue()
        producer_running = True
        
        def producer(url=None, movie_id=None, page_max=50, page=0):
            nonlocal producer_running
            if producer_running is True and page <= page_max:
                movie_url = None
                if movie_id is not None:
                    movie_url = 'https://movie.douban.com/subject/{}/comments'.format(str(movie_id))
                else:
                    movie_url = url
                print("开始爬取第{0}页***********************************************************************：".format(page+1))
                params={
                    'start':page*20,
                    'limit':20,
                    'status':'P',
                    'sort':'new_score'
                }
                html = self.session_get(movie_url, params=params)
                soup = BeautifulSoup(html.content, 'html.parser')
                comments = soup.find(id='comments').find_all(class_='comment-item')
                if len(comments) > 1:
                    queue.put(comments)
                    producer(url=movie_url, page=page+1, page_max=page_max)
                else:
                    producer_running=False
            else:
                producer_running=False
            
        def customer():
            nonlocal count
            while producer_running is True or queue.empty() is False:
                comments = queue.get()
                for comment in comments:
                    content = comment.find(class_='comment-content').text
                    user_name = comment.find(class_='comment-info').a.text
                    comment_time = comment.find(class_='comment-info').find(class_='comment-time').attrs['title']
                    print('comment:{}, user_name:{}, comment_time:{}'.format(content,user_name,comment_time))
                    count += 1
                print("count={}".format(count))
                time.sleep(int(random.choice([0.5, 0.2, 0.3])))
                
        threads = list()
        
        thread_p = threading.Thread(target=producer, kwargs=kwargs)
        thread_p.start()
        threads.append(thread_p)
        
        for _ in range(10):
            thread_c = threading.Thread(target=customer)
            thread_c.start()
            threads.append(thread_c)
            
        for thread in threads:
            thread.join(timeout=0.5)