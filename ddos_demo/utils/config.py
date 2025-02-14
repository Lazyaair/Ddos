import yaml
import os

class Config:
    def __init__(self, config_file="config.yaml"):
        self.config_file = config_file
        self.default_config = {
            'defense': {
                'traffic_clean': {
                    'threshold': 1000,
                    'window_size': 10,
                },
                'access_control': {
                    'max_requests': 100,
                    'window_size': 60,
                    'reputation_threshold': -10,
                }
            },
            'attack': {
                'threads': 4,
                'delay': {
                    'min': 0.01,
                    'max': 0.05
                }
            },
            'monitor': {
                'stats_interval': 1
            }
        }
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        else:
            self.save_config(self.default_config)
            return self.default_config
    
    def save_config(self, config):
        """保存配置到文件"""
        with open(self.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    
    def get(self, key, default=None):
        """获取配置项"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default 