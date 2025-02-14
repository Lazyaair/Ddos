import time
from collections import defaultdict
import threading
from utils.monitor import AttackMonitor

class TrafficCleaner:
    def __init__(self):
        self.ip_counter = defaultdict(int)
        self.packet_stats = defaultdict(int)
        self.threshold = 1000  # 每秒包数阈值
        self.window_size = 10  # 统计窗口(秒)
        self.blacklist = set()
        self.lock = threading.Lock()
        self.monitor = AttackMonitor()
        self.running = False
    
    def analyze_packet(self, packet):
        """分析数据包特征"""
        if hasattr(packet, 'src') and packet.src:
            with self.lock:
                self.ip_counter[packet.src] += 1
                
                # 检查是否超过阈值
                if self.ip_counter[packet.src] > self.threshold:
                    self.blacklist.add(packet.src)
                    return False
        
        # 检查TCP SYN Flood
        if packet.haslayer('TCP') and packet['TCP'].flags == 'S':
            self.packet_stats['syn_packets'] += 1
            
        # 检查ICMP Flood
        if packet.haslayer('ICMP'):
            self.packet_stats['icmp_packets'] += 1
            
        # 检查DNS放大攻击
        if packet.haslayer('DNS'):
            self.packet_stats['dns_packets'] += 1
        
        return True
    
    def clean_traffic(self, packet):
        """流量清洗"""
        if packet.src in self.blacklist:
            self.monitor.update_stats("blocked_packets", 1)
            return False
            
        if self.analyze_packet(packet):
            return True
        return False
    
    def start_cleaning(self):
        """开始流量清洗"""
        self.running = True
        
        # 启动统计重置线程
        def reset_stats():
            while self.running:
                time.sleep(self.window_size)
                with self.lock:
                    self.ip_counter.clear()
                    self.packet_stats.clear()
        
        thread = threading.Thread(target=reset_stats)
        thread.daemon = True
        thread.start()
        
        return thread
    
    def stop_cleaning(self):
        """停止流量清洗"""
        self.running = False
        return self.monitor.get_stats() 