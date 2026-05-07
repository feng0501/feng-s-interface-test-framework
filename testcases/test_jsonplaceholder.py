# testcases/real_api/test_jsonplaceholder.py
import allure
import pytest
from common.api_client import ApiClient

api = ApiClient()


@allure.feature("JSONPlaceholder 真实API测试")
class TestJSONPlaceholder:

    @allure.story("查询帖子")
    @allure.title("获取所有帖子，验证返回列表")
    def test_get_all_posts(self):
        with allure.step("发送GET请求 /posts"):
            response = api.get("/posts")
            allure.attach(str(response.status_code), name="状态码", attachment_type=allure.attachment_type.TEXT)
        with allure.step("验证状态码200"):
            assert response.status_code == 200
        with allure.step("验证返回数据为列表且不为空"):
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0

    @allure.story("查询帖子")
    @allure.title("获取ID为1的帖子，验证内容结构")
    def test_get_one_post(self):
        with allure.step("发送GET请求 /posts/1"):
            response = api.get("/posts/1")
        with allure.step("验证状态码200"):
            assert response.status_code == 200
        with allure.step("验证帖子ID为1且包含必要字段"):
            data = response.json()
            assert data["id"] == 1
            assert "userId" in data
            assert "title" in data
            assert "body" in data

    @allure.story("创建帖子")
    @allure.title("创建新帖子，验证返回状态码和数据")
    def test_create_post(self):
        new_post = {"title": "foo", "body": "bar", "userId": 1}
        with allure.step(f"发送POST请求创建帖子，数据: {new_post}"):
            response = api.post("/posts", json=new_post)
        with allure.step("验证状态码201"):
            assert response.status_code == 201
        with allure.step("验证返回数据正确"):
            data = response.json()
            assert data["title"] == new_post["title"]
            assert data["body"] == new_post["body"]
            assert "id" in data