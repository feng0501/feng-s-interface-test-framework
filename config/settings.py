# config/settings.py
import os

# 默认使用 Mock 服务器，可通过环境变量 BASE_URL 覆盖
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")
TIMEOUT = 10

# 天气 API 专用
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")