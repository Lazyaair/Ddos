import time
from threading import Lock

class AttackMonitor:
    def __init__(self):
        self.stats = {
            "syn_flood": 0,
            "icmp_flood": 0,
            "http_flood": 0,
            "dns_amp": 0
        }
        self.start_time = time.time()
        self.lock = Lock()
    
    def update_stats(self, attack_type, count):
        with self.lock:
            self.stats[attack_type] += count
    
    def get_stats(self):
        duration = time.time() - self.start_time
        with self.lock:
            return {
                "duration": duration,
                "packets_sent": self.stats,
                "packets_per_second": {
                    k: v/duration for k, v in self.stats.items() if duration > 0
                }
            }
    
    def start_monitoring(self):
        while True:
            time.sleep(1)
            stats = self.get_stats()
            print(f"\r攻击状态: {stats['packets_per_second']} 包/秒", end="") 