# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QichachaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # name = scrapy.Field()
    company_name = scrapy.Field()  #公司名字
    credit_number = scrapy.Field() #统一社会信用代码
    shareholder = scrapy.Field()  #股东姓名
    shareholding_ratio = scrapy.Field()  #持股比例
    subscription_capital = scrapy.Field() #认缴出资额
    subscription_date = scrapy.Field() #认缴出资日期
    number_of_shares = scrapy.Field() #持股数
    zz_shareholding_ratio = scrapy.Field()#最终受益股份
