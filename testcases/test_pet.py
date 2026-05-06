# testcases/test_pet.py
import pytest
import time
import allure
import os
from common.api_client import ApiClient
from common.logger import logger
from common.utils import load_yaml

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
api = ApiClient()

@allure.feature("宠物管理")
@allure.story("查询宠物")
@allure.title("通过存在的ID查询宠物")

def test_get_pet_by_id():
    pet_id = 1
    response = api.get(f"/pet/{pet_id}")
    logger.info(f"GET /pet/{pet_id} 响应状态码: {response.status_code}")
    # 断言
    assert response.status_code == 200
    assert response.json()["id"] == pet_id
    assert "name" in response.json()

def test_add_new_pet():
    pet_data = {
        "id": 100,
        "name": "毛毛",
        "photoUrls": ["string"],
        "status": "available"
    }
    response = api.post("/pet", json=pet_data)
    assert response.status_code == 200
    assert response.json()["name"] == "毛毛"
    assert response.json()["id"] == 100

    # 查询一下，确认添加成功
    get_response = api.get("/pet/100")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "毛毛"


def test_delete_pet_then_get_404():
    # 第一步：先新增一个宠物
    new_pet = {
        "id": 999,
        "name": "tobedeleted",
        "photoUrls": [],
        "status": "available"
    }
    add_resp = api.post("/pet", json=new_pet)
    assert add_resp.status_code == 200

    # 第二步：删除这个宠物
    del_resp = api.delete(f"/pet/{new_pet['id']}")
    assert del_resp.status_code == 204  # 204 表示删除成功无返回体

    # 第三步：再次查询这个宠物，应该返回 404
    get_resp = api.get(f"/pet/{new_pet['id']}")
    assert get_resp.status_code == 404
    # 可选：验证错误消息
    assert get_resp.json()["message"] == "Pet not found"


def test_delete_nonexistent_pet():
    # 用当前时间戳作为ID，几乎不会与已有数据冲突
    fake_id = int(time.time()) + 100000
    resp = api.delete(f"/pet/{fake_id}")
    assert resp.status_code == 404
    # 可选：检查错误消息
    assert resp.json().get("message") == "Pet not found"

@allure.feature("宠物管理")
@allure.story("新增宠物")
@pytest.mark.parametrize("case", load_yaml(os.path.join(DATA_DIR, "pet_data.yaml"))["test_add_pets"])
def test_add_pet_parametrized(case):
    pet_data = {
        "id": case["id"],
        "name": case["name"],
        "photoUrls": case["photoUrls"],
        "status": case["status"]
    }
    logger.info(f"正在测试: {case['case_name']}, 数据: {pet_data}")
    response = api.post("/pet", json=pet_data)
    assert response.status_code == 200
    assert response.json()["id"] == case["id"]
    assert response.json()["name"] == case["name"]
    assert response.json()["status"] == case["status"]

# ====================== 更新宠物接口测试 ======================
@pytest.mark.parametrize("case", load_yaml("data/pet_data.yaml")["put_update_cases"])
def test_update_pet(case):
    # 1. 准备阶段：先创建一个宠物
    create_resp = api.post("/pet", json=case["create_data"])
    assert create_resp.status_code == 200
    # 2. 测试阶段：更新宠物信息
    pet_id = case["update_data"]["id"]
    update_resp = api.put(f"/pet/{pet_id}", json=case["update_data"])
    assert update_resp.status_code == 200
    # 校验返回的结果是否与更新数据一致
    assert update_resp.json() == case["update_data"]
    # 3. 验证阶段：再次查询宠物的信息
    get_resp = api.get(f"/pet/{pet_id}")
    assert get_resp.status_code == 200
    # 校验查询到的结果是否已成功更新
    assert get_resp.json() == case["update_data"]