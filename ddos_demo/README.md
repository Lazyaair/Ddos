# DDoS 攻防演示系统

## 系统功能介绍

### 1. 攻击模块
- **网络层攻击**
  - SYN Flood：通过发送大量SYN请求耗尽目标服务器的半连接队列
  - ICMP Flood：发送大量ICMP Echo请求消耗网络带宽
- **应用层攻击**
  - HTTP Flood：发送大量HTTP GET/POST请求耗尽Web服务器资源
  - DNS Amplification：利用DNS服务器放大攻击流量

### 2. 防御模块
- **流量清洗**
  - 流量特征分析：识别异常流量模式
  - IP行为分析：监控源IP的请求行为
  - 动态阈值控制：自适应调整清洗策略
- **访问控制**
  - IP信誉度机制：记录和评估IP行为
  - 请求频率限制：控制单IP访问速率
  - 动态黑白名单：自动更新IP过滤规则

## 使用参数说明

### 攻击命令 (attack_cli.py)
bash
usage: attack_cli.py [-h] -t TARGET [-p PORT] -m {syn,icmp,http,dns}
[--threads THREADS] [--duration DURATION]
[--http-method {GET,POST}]
参数说明：
-t, --target 目标IP或域名
-p, --port 目标端口号 (默认: 80)
-m, --mode 攻击模式: syn/icmp/http/dns
--threads 攻击线程数 (默认: 4)
--duration 持续时间(秒) (默认: 10)
--http-method HTTP方法 (默认: GET)

### 防御命令 (defense_cli.py)

bash
usage: defense_cli.py [-h] [-i INTERFACE] -m {traffic,access,all}
[--threshold THRESHOLD] [--window WINDOW] [--report]
参数说明：
-i, --interface 监听网络接口 (默认: eth0)
-m, --mode 防御模式: traffic/access/all
--threshold 流量阈值(包/秒) (默认: 1000)
--window 统计窗口(秒) (默认: 60)
--report 生成防御报告

## 目录结构及核心实现
ddos_demo/
├── attack/ # 攻击模块
│ ├── network/ # 网络层攻击
│ │ ├── syn_flood.py # SYN洪水攻击实现
│ │ └── icmp_flood.py # ICMP洪水攻击实现
│ └── application/ # 应用层攻击
│ ├── http_flood.py # HTTP洪水攻击实现
│ └── dns_amp.py # DNS放大攻击实现
├── defense/ # 防御模块
│ ├── traffic_clean.py # 流量清洗实现
│ └── access_control.py # 访问控制实现
├── utils/ # 工具模块
│ ├── monitor.py # 攻击效果监控
│ ├── logger.py # 日志记录
│ ├── config.py # 配置管理
│ └── report.py # 报告生成
├── attack_cli.py # 攻击命令行入口
└── defense_cli.py # 防御命令行入口

## 核心实现逻辑

### 1. 攻击模块核心实现
- **SYN Flood**
  ```python
  # 核心逻辑：构造TCP SYN包并发送
  ip_packet = IP(src=source_ip, dst=target_ip)
  tcp_packet = TCP(sport=source_port, dport=target_port, flags="S")
  send(ip_packet/tcp_packet)
  ```

- **HTTP Flood**
  ```python
  # 核心逻辑：发送HTTP请求
  session.get/post(target_url, 
                  headers=random_headers,
                  data=random_data)
  ```

### 2. 防御模块核心实现
- **流量清洗**
  ```python
  # 核心逻辑：分析和过滤数据包
  def clean_traffic(self, packet):
      if packet.src in self.blacklist:
          return False
      if self.analyze_packet(packet):
          return True
      return False
  ```

- **访问控制**
  ```python
  # 核心逻辑：IP信誉度检查
  def check_ip_reputation(self, ip):
      if ip in self.blacklist:
          return False
      return self.ip_reputation.get(ip, 0) > self.threshold
  ```

### 3. 监控系统实现
```python
# 核心逻辑：统计和监控
def update_stats(self, attack_type, count):
    with self.lock:
        self.stats[attack_type] += count
```

### 4. 多线程实现
```python
# 核心逻辑：并发攻击
def start_attack(self):
    threads = []
    for _ in range(self.num_threads):
        thread = threading.Thread(target=self.attack_method)
        thread.start()
        threads.append(thread)
    return threads
```

## 使用示例

1. 启动SYN Flood攻击：
```bash
sudo python3 attack_cli.py -t 192.168.1.1 -m syn --threads 8
```

2. 启动防御系统：
```bash
sudo python3 defense_cli.py -m all --threshold 500 --report
```

## 依赖安装
```bash
sudo pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple matplotlib pandas scapy requests fake-useragent pyyaml
```