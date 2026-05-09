# 接口自动化测试框架

基于 Python + Pytest + Requests 的全功能接口自动化测试框架，支持 Mock 服务、数据驱动、Allure 报告、Docker 容器化及 CI/CD 集成。

## 技术栈

- **语言**：Python 3.12
- **测试框架**：Pytest
- **HTTP 客户端**：Requests
- **Mock 服务**：Flask
- **数据驱动**：PyYAML
- **测试报告**：Allure
- **容器化**：Docker + Docker Compose
- **持续集成**：GitHub Actions
- **版本控制**：Git

## 快速开始

### 1. 环境要求

- Python 3.12+
- Docker Desktop（可选，用于容器化运行）
- Allure 命令行（用于生成报告）

### 2. 本地运行（不使用 Docker）

```bash
# 安装依赖
pip install -r requirements.txt

# 启动 Mock 服务器（终端1）
python mock_server.py

# 运行测试并生成 Allure 结果（终端2）
pytest testcases/ --alluredir=./reports/allure_raw

# 生成 HTML 报告
allure generate ./reports/allure_raw -o ./reports/allure_html --clean

# 打开报告
allure open ./reports/allure_html