# common/api_client.py
import requests
from config.settings import BASE_URL, TIMEOUT
import allure
import json

class ApiClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        # 附加请求信息
        allure.attach(f"{method} {url}\nParams: {kwargs.get('params')}\nBody: {kwargs.get('json')}",
                      name=f"Request {method} {endpoint}",
                      attachment_type=allure.attachment_type.TEXT)

        response = self.session.request(method, url, **kwargs)

        # 附加响应信息
        try:
            response_body = response.json()
            allure.attach(json.dumps(response_body, indent=2),
                          name=f"Response {response.status_code}",
                          attachment_type=allure.attachment_type.JSON)
        except:
            allure.attach(response.text,
                          name=f"Response {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)
        return response

    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)