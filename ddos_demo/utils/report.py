import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

class DefenseReport:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        self.attack_stats = []
        self.defense_stats = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def add_stats(self, attack_stat, defense_stat):
        """添加统计数据"""
        self.attack_stats.append(attack_stat)
        self.defense_stats.append(defense_stat)
    
    def generate_plots(self):
        """生成统计图表"""
        # 攻击包统计
        plt.figure(figsize=(10, 6))
        for stat in self.attack_stats:
            plt.plot(stat['packets_per_second'].values())
        plt.title('Attack Packets per Second')
        plt.xlabel('Time')
        plt.ylabel('Packets/s')
        plt.savefig(os.path.join(self.output_dir, f'attack_stats_{self.timestamp}.png'))
        
        # 防御效果统计
        plt.figure(figsize=(10, 6))
        blocked = [stat['blocked_packets'] for stat in self.defense_stats]
        plt.bar(range(len(blocked)), blocked)
        plt.title('Blocked Packets')
        plt.xlabel('Time Window')
        plt.ylabel('Packets')
        plt.savefig(os.path.join(self.output_dir, f'defense_stats_{self.timestamp}.png'))
    
    def generate_report(self):
        """生成防御报告"""
        report_file = os.path.join(self.output_dir, f'report_{self.timestamp}.html')
        
        # 生成统计图表
        self.generate_plots()
        
        # 计算防御效果
        total_attack_packets = sum(sum(stat['packets_sent'].values()) 
                                 for stat in self.attack_stats)
        total_blocked_packets = sum(stat['blocked_packets'] 
                                  for stat in self.defense_stats)
        
        defense_rate = (total_blocked_packets / total_attack_packets 
                       if total_attack_packets > 0 else 0)
        
        # 生成HTML报告
        html_content = f"""
        <html>
        <head>
            <title>DDoS Defense Report - {self.timestamp}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .stats {{ margin: 20px 0; }}
                img {{ max-width: 800px; }}
            </style>
        </head>
        <body>
            <h1>DDoS Defense Report</h1>
            <div class="stats">
                <h2>Defense Statistics</h2>
                <p>Total Attack Packets: {total_attack_packets}</p>
                <p>Total Blocked Packets: {total_blocked_packets}</p>
                <p>Defense Rate: {defense_rate:.2%}</p>
            </div>
            <div class="plots">
                <h2>Attack Statistics</h2>
                <img src="attack_stats_{self.timestamp}.png">
                <h2>Defense Statistics</h2>
                <img src="defense_stats_{self.timestamp}.png">
            </div>
        </body>
        </html>
        """
        
        with open(report_file, 'w') as f:
            f.write(html_content)
        
        return report_file 