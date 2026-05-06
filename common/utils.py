import yaml
import os

def load_yaml(file_path):
    """加载YAML文件并返回内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)