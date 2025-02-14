from attack.network.syn_flood import SYNFlood
from attack.network.icmp_flood import ICMPFlood
from attack.application.http_flood import HTTPFlood
from attack.application.dns_amp import DNSAmplification
from defense.traffic_clean import TrafficCleaner
from defense.access_control import AccessController
from utils.logger import DDoSLogger
from utils.config import Config
from utils.report import DefenseReport
import time
import threading

def test_attack_with_defense(attack_obj, defense_obj, logger, report):
    """测试攻击效果和防御效果"""
    logger.info(f"开始测试 {attack_obj.__class__.__name__}...")
    
    # 启动防御
    defense_thread = defense_obj.start_cleaning()
    time.sleep(1)  # 等待防御系统就绪
    
    # 启动攻击
    attack_threads = attack_obj.start_attack()
    
    # 运行指定时间
    duration = config.get('attack.duration', 10)
    time.sleep(duration)
    
    # 停止攻击和防御
    attack_stats = attack_obj.stop_attack()
    defense_stats = defense_obj.stop_cleaning()
    
    # 等待所有线程结束
    for thread in attack_threads:
        thread.join()
    defense_thread.join()
    
    # 记录统计信息
    logger.info(f"\n攻击统计:\n{attack_stats}")
    logger.info(f"\n防御统计:\n{defense_stats}")
    
    # 添加到报告
    report.add_stats(attack_stats, defense_stats)

def main():
    # 初始化配置、日志和报告系统
    config = Config()
    logger = DDoSLogger()
    report = DefenseReport()
    
    target_ip = config.get('target.ip', "127.0.0.1")
    target_port = config.get('target.port', 80)
    
    # 初始化防御系统
    traffic_cleaner = TrafficCleaner()
    access_controller = AccessController()
    
    # 测试各种攻击和防御效果
    attacks = [
        SYNFlood(target_ip, target_port),
        ICMPFlood(target_ip),
        HTTPFlood("http://127.0.0.1", attack_type="GET"),
        DNSAmplification(target_ip)
    ]
    
    for attack in attacks:
        test_attack_with_defense(attack, traffic_cleaner, logger, report)
        time.sleep(2)  # 间隔时间
    
    # 生成报告
    report_file = report.generate_report()
    logger.info(f"防御报告已生成: {report_file}")

if __name__ == "__main__":
    main() 