# testcases/real_api/test_weather.py
import allure
import pytest
import requests
from config import settings


@allure.feature("OpenWeatherMap 真实API")
class TestWeather:

    @allure.story("查询天气")
    @allure.title("查询伦敦当前天气，验证返回数据结构")
    def test_get_weather_in_london(self):
        url = f"{settings.BASE_URL}/data/2.5/weather"
        params = {
            "q": "London",
            "appid": settings.WEATHER_API_KEY,
            "units": "metric"
        }
        with allure.step(f"发送GET请求到 {url}，参数q=London"):
            response = requests.get(url, params=params)
            allure.attach(str(response.status_code), name="状态码", attachment_type=allure.attachment_type.TEXT)
            allure.attach(response.text, name="响应JSON", attachment_type=allure.attachment_type.JSON)
        with allure.step("验证状态码200"):
            assert response.status_code == 200
        with allure.step("验证城市名称为London"):
            data = response.json()
            assert data["name"] == "London"
        with allure.step("验证包含main和temp字段"):
            assert "main" in data
            assert "temp" in data["main"]

    @allure.story("查询天气")
    @allure.title("查询不存在的城市，应返回404")
    def test_get_weather_in_invalid_city(self):
        url = f"{settings.BASE_URL}/data/2.5/weather"
        params = {
            "q": "ThisCityDoesNotExistXYZ",
            "appid": settings.WEATHER_API_KEY
        }
        with allure.step("发送GET请求到错误城市"):
            response = requests.get(url, params=params)
        with allure.step("验证返回404"):
            assert response.status_code == 404
            assert response.json()["message"] == "city not found"