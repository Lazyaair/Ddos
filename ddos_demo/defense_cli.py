#!/usr/bin/env python3
import argparse
from defense.traffic_clean import TrafficCleaner
from defense.access_control import AccessController
from utils.logger import DDoSLogger
from utils.config import Config
from utils.report import DefenseReport
import time
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='DDoS防御系统')
    parser.add_argument('-i', '--interface', default='eth0',
                      help='监听网络接口 (默认: eth0)')
    parser.add_argument('-m', '--mode', required=True, 
                      choices=['traffic', 'access', 'all'],
                      help='防御模式: traffic(流量清洗), access(访问控制), all(全部)')
    parser.add_argument('--threshold', type=int, default=1000,
                      help='流量阈值(包/秒) (默认: 1000)')
    parser.add_argument('--window', type=int, default=60,
                      help='统计窗口大小(秒) (默认: 60)')
    parser.add_argument('--report', action='store_true',
                      help='生成防御报告')
    return parser.parse_args()

def main():
    args = parse_args()
    config = Config()
    logger = DDoSLogger()
    
    if args.report:
        report = DefenseReport()
    
    logger.info(f"启动DDoS防御系统...")
    logger.info(f"监听接口: {args.interface}")
    logger.info(f"防御模式: {args.mode}")
    logger.info(f"流量阈值: {args.threshold} 包/秒")
    logger.info(f"统计窗口: {args.window} 秒")
    
    try:
        # 初始化防御模块
        if args.mode in ['traffic', 'all']:
            traffic_cleaner = TrafficCleaner()
            traffic_cleaner.threshold = args.threshold
            traffic_cleaner.window_size = args.window
            traffic_thread = traffic_cleaner.start_cleaning()
        
        if args.mode in ['access', 'all']:
            access_controller = AccessController()
            access_controller.window_size = args.window
            access_thread = access_controller.start_control()
        
        # 保持程序运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n用户停止防御")
        
        # 停止防御并生成报告
        if args.mode in ['traffic', 'all']:
            stats = traffic_cleaner.stop_cleaning()
            if args.report:
                report.add_stats({'packets_sent': {}}, stats)
        
        if args.mode in ['access', 'all']:
            access_controller.stop_control()
        
        if args.report:
            report_file = report.generate_report()
            logger.info(f"防御报告已生成: {report_file}")
        
    except Exception as e:
        logger.error(f"防御系统运行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 