#!/usr/bin/env python
# -*- coding:utf-8-*-

import requests
from bs4 import BeautifulSoup
import re
import json

from cat_brand.Car import out_of_market_cars_html
from cat_brand.NewCar import on_market_cars_html


"""
汽车品牌整体解析的代码

"""

# 起始页面
# 26个字母
start_url = 'https://www.autohome.com.cn/grade/carhtml/A_photo.html'

response= requests.get(start_url)

soup = BeautifulSoup(response.text, "lxml")

dl_A_brands = soup.find_all("dl")

all_car = {}

car_brand_arr = []

for brand in dl_A_brands:
    car_brand_dict = {}

    # 首先是品牌区
    brand_id = brand["id"]
    brand_olr = brand["olr"]
    brand_img = "https:" + brand.find("dt").find("img")["src"]
    brand_name = brand.find("dt").find("div").string
   # print(brand_id, brand_img, brand_name)

    # 添加品牌数据到字典中
    car_brand_dict["brand_id"] = brand_id
    car_brand_dict["brand_olr"] = brand_olr
    car_brand_dict["brand_img"] = brand_img
    car_brand_dict["brand_name"] = brand_name


    # 然后是车型区
    # 获取所有子品牌
    son_brand_content = brand.find("dd")
    son_brands = son_brand_content.find_all("div", class_="h3-tit")

    # 获取车辆列表
    car_type_colletions = brand.find_all("ul", class_='rank-img-ul')
    # print("车辆列表：", car_type_colletions)

    # 车型数据列表
    for i in range(0, len(son_brands)):
        # 获取子品牌名称
        son_brand_in = son_brands[i]
        son_brand = son_brand_in.string
        # 获取子品牌内的车型
        car_list = car_type_colletions[i]
        # print("-------------\n",car_list,"\n------------\n")
        car_list_arr = []
        for li in car_list.find_all("li"):
            car_type = {}
            # print(li.attrs)
            if 'class' in li.attrs:
                #if 'dashline' == li.attrs['class']:
                continue
            car_id = li["id"]
            car_link = li.find("a")["href"]
            car_name = li.find("a").string
            car_img = "https:" + li.find("img")["src"]
            car_price_a = li.find("a", class_="red")
            car_price = '未知'
            if car_price_a is not None:
                car_price = car_price_a.string

            # print(car_id, car_link, car_name, car_img, car_price)

            # 添加车型数据列表
            car_type["car_id"] = car_id.replace("s", "")
            car_type["car_link"] = "https:" + car_link
            car_type["car_name"] = car_name
            car_type["car_img"] = car_img
            car_type["car_price"] = car_price

            # print(car_id)

            # TODO：开始解析车型数据
            print("当前请求链接为：", car_type["car_link"])
            response_car = requests.get(car_type["car_link"])
            out_of_market_cars = out_of_market_cars_html(response_car.text, car_type["car_id"])
            on_market_cars = on_market_cars_html(response_car.text)

            car_type["out_of_market_cars"] = out_of_market_cars
            car_type["on_market_cars"] = on_market_cars

            car_list_arr.append(car_type)

            # print(json.dumps(car_list_arr))

        car_brand_dict["car_types"] = car_list_arr
    car_brand_arr.append(car_brand_dict)

all_car["A"] = car_brand_arr

print(json.dumps(all_car))
