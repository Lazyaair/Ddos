import time
from collections import defaultdict
import threading
import ipaddress

class AccessController:
    def __init__(self):
        self.ip_reputation = {}  # IP信誉度记录
        self.request_count = defaultdict(int)  # IP请求计数
        self.blacklist = set()  # 黑名单
        self.whitelist = set()  # 白名单
        self.lock = threading.Lock()
        self.running = False
        
        # 配置参数
        self.max_requests = 100  # 每个时间窗口内的最大请求数
        self.window_size = 60  # 时间窗口大小(秒)
        self.reputation_threshold = -10  # 信誉度阈值
    
    def check_ip_reputation(self, ip):
        """检查IP信誉度"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            # 检查是否是私有IP
            if ip_obj.is_private:
                return True
                
            with self.lock:
                # 检查白名单
                if ip in self.whitelist:
                    return True
                    
                # 检查黑名单
                if ip in self.blacklist:
                    return False
                    
                # 检查信誉度
                reputation = self.ip_reputation.get(ip, 0)
                return reputation > self.reputation_threshold
        except ValueError:
            return False
    
    def update_ip_reputation(self, ip, score_delta):
        """更新IP信誉度"""
        with self.lock:
            current_score = self.ip_reputation.get(ip, 0)
            new_score = current_score + score_delta
            self.ip_reputation[ip] = new_score
            
            # 根据信誉度更新黑白名单
            if new_score < self.reputation_threshold:
                self.blacklist.add(ip)
            elif new_score > 10:
                self.whitelist.add(ip)
    
    def check_rate_limit(self, ip):
        """检查请求频率限制"""
        with self.lock:
            self.request_count[ip] += 1
            return self.request_count[ip] <= self.max_requests
    
    def start_control(self):
        """启动访问控制"""
        self.running = True
        
        def reset_counters():
            while self.running:
                time.sleep(self.window_size)
                with self.lock:
                    self.request_count.clear()
        
        thread = threading.Thread(target=reset_counters)
        thread.daemon = True
        thread.start()
        
        return thread
    
    def stop_control(self):
        """停止访问控制"""
        self.running = False 