# -*- coding: utf-8 -*-
from scrapy.cmdline import execute
import csv


#清空文件内容

def czResultFile():

    lstitle1 = ['公司名字','统一社会信用代码','股东姓名','持股比例','认缴出资额','认缴出资日期']
    lstitle2 = ['公司名字','统一社会信用代码','股东姓名','持股比例','持股数']
    with open('../result/shareholder.csv','a+',newline='',encoding='utf-8') as f1,open('../result/shareholdernew.csv','a+',newline='',encoding='utf-8') as f2:
        f1.seek(0)
        f1.truncate()
        csvfile1 = csv.writer(f1)
        csvfile1.writerow(lstitle1)
        f2.seek(0)
        f2.truncate()
        csvfile2 = csv.writer(f2)
        csvfile2.writerow(lstitle2)



if __name__ == '__main__':
    czResultFile()
    execute(['scrapy', 'crawl', 'qcc'])