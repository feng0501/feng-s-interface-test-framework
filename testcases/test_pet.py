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


@allure.feature("宠物管理模块")
class TestPet:

    @allure.story("查询宠物")
    @allure.title("通过存在的ID查询宠物")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_pet_by_id(self):
        pet_id = 1
        with allure.step(f"发送GET请求查询宠物ID {pet_id}"):
            response = api.get(f"/pet/{pet_id}")
            allure.attach(str(response.status_code), name="状态码", attachment_type=allure.attachment_type.TEXT)
            allure.attach(response.text, name="响应内容", attachment_type=allure.attachment_type.JSON)
            logger.info(f"GET /pet/{pet_id} 响应状态码: {response.status_code}")
        with allure.step("验证响应状态码为200"):
            assert response.status_code == 200
        with allure.step("验证返回的宠物ID正确"):
            assert response.json()["id"] == pet_id
        with allure.step("验证响应中包含name字段"):
            assert "name" in response.json()

    @allure.story("新增宠物")
    @allure.title("新增一个宠物并验证查询成功")
    def test_add_new_pet(self):
        pet_data = {
            "id": 100,
            "name": "毛毛",
            "photoUrls": ["string"],
            "status": "available"
        }
        with allure.step(f"发送POST请求新增宠物 {pet_data}"):
            response = api.post("/pet", json=pet_data)
            allure.attach(str(response.status_code), name="状态码", attachment_type=allure.attachment_type.TEXT)
            allure.attach(response.text, name="响应内容", attachment_type=allure.attachment_type.JSON)
        with allure.step("验证新增成功状态码200"):
            assert response.status_code == 200
        with allure.step("验证返回的name和id正确"):
            assert response.json()["name"] == "毛毛"
            assert response.json()["id"] == 100
        with allure.step("查询刚刚新增的宠物验证存在"):
            get_response = api.get("/pet/100")
            assert get_response.status_code == 200
            assert get_response.json()["name"] == "毛毛"

    @allure.story("删除宠物")
    @allure.title("新增一个宠物，删除后查询应返回404")
    def test_delete_pet_then_get_404(self):
        new_pet = {
            "id": 999,
            "name": "tobedeleted",
            "photoUrls": [],
            "status": "available"
        }
        with allure.step(f"新增宠物 {new_pet}"):
            add_resp = api.post("/pet", json=new_pet)
            assert add_resp.status_code == 200
        with allure.step(f"删除宠物ID {new_pet['id']}"):
            del_resp = api.delete(f"/pet/{new_pet['id']}")
            assert del_resp.status_code == 204
        with allure.step("查询已删除的宠物，预期404"):
            get_resp = api.get(f"/pet/{new_pet['id']}")
            assert get_resp.status_code == 404
            assert get_resp.json()["message"] == "Pet not found"

    @allure.story("删除宠物")
    @allure.title("删除不存在的宠物ID应返回404")
    def test_delete_nonexistent_pet(self):
        fake_id = int(time.time()) + 100000
        with allure.step(f"删除不存在的宠物ID {fake_id}"):
            resp = api.delete(f"/pet/{fake_id}")
        with allure.step("验证返回404"):
            assert resp.status_code == 404
            assert resp.json().get("message") == "Pet not found"

    @allure.story("新增宠物")
    @allure.title("参数化新增宠物测试")
    @pytest.mark.parametrize("case", load_yaml(os.path.join(DATA_DIR, "pet_data.yaml"))["test_add_pets"])
    def test_add_pet_parametrized(self, case):
        allure.dynamic.title(f"新增宠物 - {case['case_name']}")
        pet_data = {
            "id": case["id"],
            "name": case["name"],
            "photoUrls": case["photoUrls"],
            "status": case["status"]
        }
        with allure.step(f"请求参数: {pet_data}"):
            response = api.post("/pet", json=pet_data)
            allure.attach(response.text, name="响应", attachment_type=allure.attachment_type.JSON)
        with allure.step("验证状态码200"):
            assert response.status_code == 200
        with allure.step("验证返回数据与请求一致"):
            assert response.json()["id"] == case["id"]
            assert response.json()["name"] == case["name"]
            assert response.json()["status"] == case["status"]

    @allure.story("更新宠物")
    @allure.title("参数化更新宠物测试")
    @pytest.mark.parametrize("case", load_yaml(os.path.join(DATA_DIR, "pet_data.yaml"))["put_update_cases"])
    def test_update_pet(self, case):
        allure.dynamic.title(f"更新宠物 - {case['case_name']}")
        with allure.step(f"创建初始宠物: {case['create_data']}"):
            create_resp = api.post("/pet", json=case["create_data"])
            assert create_resp.status_code == 200
        with allure.step(f"更新宠物数据: {case['update_data']}"):
            pet_id = case["update_data"]["id"]
            update_resp = api.put(f"/pet/{pet_id}", json=case["update_data"])
            assert update_resp.status_code == 200
            assert update_resp.json() == case["update_data"]
        with allure.step("验证更新结果"):
            get_resp = api.get(f"/pet/{pet_id}")
            assert get_resp.status_code == 200
            assert get_resp.json() == case["update_data"]