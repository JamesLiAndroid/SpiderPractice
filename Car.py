#!/usr/bin/env python
# -*- coding:utf-8-*-
import json

import requests
from bs4 import BeautifulSoup


start_url = "https://www.autohome.com.cn/3170/"

car_id = "3170"

car_out_market_url = "https://www.autohome.com.cn/19/#levelsource=000000000_0&pvareaid=102538"

def car_out_Market(html_content):
    """
    解析停售车型的方法，该车型无当年款，已经退市

    :param html_content:
    :return:
    """
    # print(html_content)
    soup_header = BeautifulSoup(html_content, "lxml")
    title_content = soup_header.find("div", class_="title")

    car_type_marks = title_content.find("div", class_="title-subcnt-tab").ul.find_all("li")

    # 解析年款信息
    car_types = []
    for type_li in car_type_marks:
        content = type_li.find("a").string
        car_types.append(content)

    # 解析具体的车型信息
    tab_wraps = title_content.find_all("div", class_="tabwrap")
    for i in range(0, len(tab_wraps)):
        pass

    print(tab_wraps, len(tab_wraps))
    return html_content


def out_of_market_cars_html(html_content, car_id):
    """
    解析停售车型的方法

    不需要先请求车型页面

    获取停售车型的信息，构造字典数据返回

    html_content: 当前html页面内容
    car_id: 车型id

    """

    end_type_urls = "https://www.autohome.com.cn/ashx/series_allspec.ashx"

    soup_root = BeautifulSoup(html_content, "lxml")

    car_type_all = soup_root.find("div", class_="tab tab02 tab-ys")

    if car_type_all is None:
        # 当前页面为停售款页面，车型已经下线，不再胜场当年款
        old_out_of_market = car_out_Market(html_content)
        return old_out_of_market

    # 解析停售款的链接，该车型当年款尚在市场销售
    end_type_datas = car_type_all.find("div", id="drop2").find("ul")

    if end_type_datas is None:
        # 不存在车型信息，返回数据
        return "尚无该款车型信息"


    end_type_cars_num = []
    end_type_cars_year = []

    for li in end_type_datas.find_all("li"):
        a = li.find("a")
        data = a["data"]
        end_type_cars_num.append(data)

        year = a.string
        end_type_cars_year.append(year)

    # print(end_type_cars_num)
    # print(end_type_cars_year)

    # 获取停售款的车型数据
    old_car = []
    for i in range(0, len(end_type_cars_num)):
        year_replacement_num = end_type_cars_num[i]
        # year = end_type_cars_year[i]
        # 停售款车型查询需要的参数
        end_type_params = {
            "s": car_id,
            "y": year_replacement_num,
            "l": 3
        }
        response_old_car = requests.get(end_type_urls, params=end_type_params)
        # 数据清洗，去除无用的信息
        old_car_obj = json.loads(response_old_car.text)
        # print(old_car_obj)

        for spec in old_car_obj["Spec"]:
            del spec["Price2Sc"]
            del spec["Link2Sc"]
            del spec["State"]
            del spec["ShowParas"]
            del spec["ShowTaxRelief"]
            del spec["ShowPreferential"]
            del spec["videoid"]

        # 老车型添加年份数据
        #old_car_obj["year"] = year
        old_car.append(old_car_obj)

    # 添加一个key，放入字典中，转换json输出
    out_of_market_car_data = {}
    out_of_market_car_data["out_of_market"] = old_car

    print(type(json.dumps(out_of_market_car_data)))
    return out_of_market_car_data

if __name__ == '__main__':
    #response = requests.get(start_url)
    #out_of_market_cars_html(response.text, car_id)

    response = requests.get(car_out_market_url)
    car_out_Market(response.text)

# def out_of_market_cars(start_url, car_id, year):
#     """
#     解析停售车型的方法
#
#     需要先请求车型页面
#
#     获取停售车型的信息，构造字典数据返回
#
#     start_url: 获取停售车型的url
#     car_id: 车型id
#     year: 车辆年份（比如2017款， year传入2017）
#
#     """
#
#     response = requests.get(start_url)
#
#     # print(response.text)
#     soup_root = BeautifulSoup(response.text, "lxml")
#
#     car_type_all = soup_root.find("div", class_="tab tab02 tab-ys")
#
#     # print(car_type_all)
#
#     # 解析停售款的链接
#     end_type_datas = car_type_all.find("div", id="drop2").find("ul")
#
#     end_type_cars_num = []
#     for li in end_type_datas.find_all("li"):
#         a = li.find("a")
#         data = a["data"]
#         end_type_cars_num.append(data)
#
#     print(end_type_cars_num)
#
#     # 获取停售款的车型数据
#     old_car = []
#     for i in end_type_cars_num:
#         # 停售款车型查询需要的参数
#         end_type_params = {
#             "s": car_id,
#             "y": i,
#             "l": 3
#         }
#         response_old_car = requests.get(end_type_urls, params=end_type_params)
#         # 数据清洗，去除无用的信息
#         old_car_obj = json.loads(response_old_car.text)
#         # print(old_car_obj)
#
#         for spec in old_car_obj["Spec"]:
#             del spec["Price2Sc"]
#             del spec["Link2Sc"]
#             del spec["State"]
#             del spec["ShowParas"]
#             del spec["ShowTaxRelief"]
#             del spec["ShowPreferential"]
#             del spec["videoid"]
#         # 老车型添加年份数据
#         old_car_obj["year"] = year
#         old_car.append(old_car_obj)
#     #print(type(old_car), old_car)
#
#     # 添加一个key，放入字典中，转换json输出
#     out_of_market_car_data = {}
#     out_of_market_car_data["out_of_market"] = old_car
#
#     print(json.dumps(out_of_market_car_data))
#     return out_of_market_car_data
#