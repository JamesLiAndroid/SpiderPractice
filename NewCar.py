#!/usr/bin/env python
# -*- coding:utf-8-*-
import json

import requests
from bs4 import BeautifulSoup


start_url = "https://www.autohome.com.cn/3170/"

def on_market_cars_html(html_content):
    """
    解析当年款车型的方法

    start_url: 解析的页面链接

    """

    on_current_market = {}

    # response = requests.get(start_url)

    soup_root = BeautifulSoup(html_content, "lxml")

    car_type_all = soup_root.find("div", class_="tab tab02 tab-ys")

    # 解析Group数据
    div_content_item = car_type_all.find("div", class_="tab-content-item current")

    all_groups = div_content_item.find_all("div", class_="interval01-title")

    groups = []

    cars = []

    for group in all_groups:
        div_title = group.find("span", class_="interval01-list-cars-text")
        type_ul = div_title.parent.parent.find_next_sibling("ul", class_="interval01-list")

        for li in type_ul.find_all("li"):
            car_spec = {}

            info = li.find("div", class_="interval01-list-cars").find("div", class_="interval01-list-cars-infor")
            info_next = info.p.next_sibling.next_sibling.next_sibling.next_sibling
            car_group_name = div_title.string
            car_id = info.p["data-gcjid"]
            car_name = info.p.a.string
            car_driving_mode_name = info_next.span.string
            car_transmission = info_next.span.next_sibling.string
            car_price = li.find("div", class_="interval01-list-guidance").div.contents[2].strip()

    #        print(car_price_2_sc)
            car_spec["Id"] = car_id
            car_spec["Name"] = car_name
            car_spec["DrivingModeName"] = car_driving_mode_name
            car_spec["Transmission"] = car_transmission
            car_spec["Price"] = car_price
            car_spec["GroupName"] = car_group_name

            cars.append(car_spec)

        groupName = div_title.string
        groups.append(div_title.string)

    on_current_market["Group"] = groups
    on_current_market["Spec"] = cars

    # print(type(on_current_market), on_current_market)

    # 添加一个key，放入字典中，转换json输出
    on_market_car_data = {}
    on_market_car_data["on_market"] = on_current_market

    print(json.dumps(on_market_car_data))

    return on_market_car_data

if __name__ == '__main__':

    response = requests.get(start_url)
    on_market_cars_html(response.text)