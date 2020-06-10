# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv

class QichachaPipeline:
    def process_item(self, item, spider):
        if spider.name == 'qcc':

            #判断item是否有number_of_shares(持股数) 这个key
            if 'number_of_shares' in item:
                gdx = []
                company_name = item['company_name']
                credit_number = item['credit_number']
                shareholder = item['shareholder']
                shareholding_ratio = item['shareholding_ratio']
                number_of_shares = item['number_of_shares']

                gdx.append(company_name)
                gdx.append(credit_number)
                gdx.append(shareholder)
                gdx.append(shareholding_ratio)
                gdx.append(number_of_shares)

                with open('../result/shareholdernew.csv', "a+", newline='', encoding='utf8') as gdf:
                    csv_file = csv.writer(gdf)
                    csv_file.writerow(gdx)

                return item
            gdx = []
            company_name = item['company_name']
            credit_number = item['credit_number']
            shareholder = item['shareholder']
            shareholding_ratio = item['shareholding_ratio']
            subscription_capital = item['subscription_capital']
            subscription_date = item['subscription_date']

            gdx.append(company_name)
            gdx.append(credit_number)
            gdx.append(shareholder)
            gdx.append(shareholding_ratio)
            gdx.append(subscription_capital)
            gdx.append(subscription_date)

            with open('../result/shareholder.csv',"a+", newline='',encoding='utf8') as gdf:
                csv_file = csv.writer(gdf)
                csv_file.writerow(gdx)

        return item


