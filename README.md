## 技术栈
- 语言：Python 3.12
- 测试框架：Pytest
- HTTP 客户端：Requests
- Mock 服务：Flask
- 数据驱动：PyYAML
- 测试报告：Allure
- 容器化：Docker + Docker Compose
- 持续集成：GitHub Actions
- 版本控制：Git

## 快速开始
### 环境要求
- Python 3.12+（本地运行必须）
- Docker Desktop（可选，用于容器化运行）
- Allure 命令行（可选，用于生成 HTML 报告，也可只用原始数据
### 方式一：本地运行（不使用 Docker）
```bash
运行
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动 Mock 服务器（保持终端运行）
python mock_server.py

# 3. 打开另一个终端，运行测试并生成 Allure 原始数据
pytest testcases/ --alluredir=./reports/allure_raw

# 4. 生成 HTML 报告（需提前安装 Allure 命令行）
allure generate ./reports/allure_raw -o ./reports/allure_html --clean

# 5. 打开报告
allure open ./reports/allure_html

```

### 方式二：Docker 容器化运行
```bash
运行
# 1. 一键启动全部测试（宠物 + 天气）
docker-compose up --abort-on-container-exit --exit-code-from tests

# 2. 仅运行宠物测试（使用容器内 Mock）
docker-compose run --rm tests pytest testcases/test_pet.py --alluredir=/app/reports/allure_raw

# 3. 生成并查看报告（在宿主机操作，需 Allure 命令行）
allure generate ./reports/allure_raw -o ./reports/allure_html --clean
allure open ./reports/allure_html

# 4. 清理环境（停止并删除容器、网络，不删除卷）
docker-compose down
注意：请勿使用 docker-compose down -v，否则可能删除绑定的 reports 目录内容，为避免意外，建议仅使用 docker-compose down。