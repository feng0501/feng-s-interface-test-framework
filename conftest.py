# conftest.py
import pytest
import requests
import os
import allure
import time

# 定义需要特殊环境的测试模块及其对应的环境检查函数
MODULE_CHECKS = {
    "test_pet.py": lambda: _check_mock_server(),
    "test_jsonplaceholder.py": lambda: _check_base_url("jsonplaceholder.typicode.com"),
    "test_weather.py": lambda: _check_weather_api(),
}

def _check_mock_server():
    base_url = os.getenv("BASE_URL", "http://127.0.0.1:5000")
    # 最多重试 5 次，每次间隔 1 秒
    for i in range(5):
        try:
            resp = requests.get(f"{base_url}/pet/1", timeout=2)
            if resp.status_code in (200, 404):
                return True
        except:
            pass
        time.sleep(1)
    return False

def _check_base_url(expected_host):
    """检测 BASE_URL 环境变量是否指向指定的真实 API"""
    base_url = os.getenv("BASE_URL", "")
    return expected_host in base_url

def _check_weather_api():
    """检测天气 API 所需的环境变量是否设置完整"""
    base_url = os.getenv("BASE_URL", "")
    api_key = os.getenv("WEATHER_API_KEY", "")
    return "api.openweathermap.org" in base_url and api_key != ""

@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    """在收集完测试项后，根据模块和环境条件添加 skip 标记"""
    # 按测试文件分组
    module_items = {}
    for item in items:
        module_path = item.module.__file__
        module_name = os.path.basename(module_path)
        module_items.setdefault(module_name, []).append(item)

    # 对每个模块，如果环境检查失败，则给该模块所有测试项添加 skip
    for module_name, module_items_list in module_items.items():
        if module_name in MODULE_CHECKS:
            check_func = MODULE_CHECKS[module_name]
            if not check_func():
                skip_reason = f"环境不满足，跳过模块 {module_name}"
                for item in module_items_list:
                    item.add_marker(pytest.mark.skip(reason=skip_reason))

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        allure.attach(str(item.function.__doc__ or ""), name="测试描述", attachment_type=allure.attachment_type.TEXT)
        # 可以附加日志文件内容等