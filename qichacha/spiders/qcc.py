# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline
from qichacha.items import QichachaItem
import time
import logging
import json

##############
from qichacha.spcookie import fxcookie


class QccSpider(scrapy.Spider):
    name = 'qcc'
    allowed_domains = ['qcc.com']
    start_urls = ['https://www.qcc.com/search?key=']

    #如果cookie失效登录后重新获取最新的cookie

    cookies = fxcookie()

    # 重写sart_requests 函数
    def start_requests(self):
        with open('../qianti/company.txt','r',encoding='utf8') as gsf:
            for company in gsf:
                url = self.start_urls[0] + company
                print(url)
                # yield scrapy.Request(url, callback=self.parse)
                time.sleep(4)
                yield scrapy.Request(url, cookies=self.cookies, callback=self.parse)
                # yield scrapy.Request(url, cookies=self.cookies, callback=self.parse(companyname=company))

    # 提取搜索到公司的url
    def parse(self, response):
    # def parse(self, response,companyname):

        # origin = response.text
        # # origin = json.loads(response.text)['origin']
        # print('==' * 20)
        # print(origin)
        # print('==' * 20)

        time.sleep(4)
        # 提取列表中第一个公司，进入该页
        link = response.xpath('//*[@id="search-result"]/tr[1]/td[3]/a/@href').extract_first()
        detail_link = response.urljoin(link) + '#base'
        print(detail_link)
        # yield scrapy.Request(detail_link,callback=self.gd_parse)
        yield scrapy.Request(detail_link, cookies=self.cookies, callback=self.gd_parse,dont_filter=True)



    def gd_parse(self,response):

        logging.warning('11111111111111')

        # time.sleep(2)

        items = []

        print(response)


        #得到股东信息表格的内容
        table_gd = response.xpath('//*[@id="partnerslist"]/table')
        print(table_gd,'   得到股东信息表格的内容')

        # 公司名
        companyname = response.xpath('//div[@class="content"]/div[1]/h1/text()').extract_first().strip().replace('\n','')
        print(companyname, '    公司名')

        # 统一社会信用代码
        creditnumber = response.xpath('//section[@id="Cominfo"]/table[@class="ntable"]/tr[3]/td[2]/text()').extract_first().strip().replace('\n','')
        print(creditnumber, '    统一社会信用代码')

        try:
            table_gdx = table_gd[0]
        except:
            name = response.xpath('//div[@class="content"]/div[1]/h1/text()').extract_first()
            logging.warning(name + "    没有股东信息")
            return
        #得到股东信息内部的每一行的数据
        gd_list = table_gdx.xpath('./tr')


        for gd in gd_list[1:]:
            item = QichachaItem()

            item['company_name'] = companyname
            items.append(item)

            items[-1]['credit_number'] =creditnumber

            #关于公司信息标题的个数 （比如 上市信息，基本信息）
            shuliang = response.xpath('//div[@class="company-nav-contain"]/div')
            print(len(shuliang))
            shuliang = len(shuliang)

            #股东姓名
            shareholder_nm = gd.xpath('./td[2]/table/tr/td[2]/a/h3/text()').extract_first()
            if shareholder_nm == None:
                shareholder_nm = gd.xpath('./td[2]/table/tr/td[2]/div/a/h3/text()').extract_first()
                if shareholder_nm == None:
                    shareholder_nm = gd.xpath('./td[2]/table/tr/td[2]/div/h3/text()').extract_first()
            print(shareholder_nm,'股东姓名')
            items[-1]['shareholder'] = shareholder_nm

            #当shareholder_nm 为空时  说明出现新的格式,
            if shuliang ==9:

                #调用新格式 fzNewInfo 函数获取新的值
                items = self.fzNewInfo(response)

                return items

            #股份比例
            shareholding_bl =gd.xpath('./td[3]/text()').extract_first().strip()
            print(shareholding_bl, '   股份比例')
            items[-1]['shareholding_ratio'] = shareholding_bl

            #获取认缴出资额的标题
            czett = gd_list[0].xpath('./th[4]/span/text()').extract_first()
            print(czett , '  gd_parse')

            # 认缴出资日期
            subscription_dt = gd.xpath('./td[5]/text()').extract_first().strip('\t\n\r ,')
            print(subscription_dt,'    认缴出资日期')
            items[-1]['subscription_date'] = subscription_dt

            #认缴出资额
            subscription_cz = gd.xpath('./td[4]/text()').extract_first().strip('\t\n\r ,')
            print(subscription_cz,'        认缴出资额')

            # 获取认缴出资额的标题为None 需修改认缴出资额  认缴出资日期 获取位置
            if czett == None:

                # 获取认缴出资额的标题
                czett = gd_list[0].xpath('./th[5]/span/text()').extract_first()
                print(czett)
                subscription_cz = gd.xpath('./td[5]/text()').extract_first().strip('\t\n\r ,')



                # 认缴出资日期
                subscription_dt = gd.xpath('./td[6]/text()').extract_first().strip('\t\n\r ,')
                print(subscription_dt, '      认缴出资日期')
                items[-1]['subscription_date'] = subscription_dt



            if subscription_cz == '-':
                # subscription_cz = 0
                # items.pop(0)

                if shuliang == 9:
                    # 调用新格式 fzNewInfo 函数获取新的值
                    items = self.fzNewInfo(response)

                    return items
                subscription_cz = 0


            if '(万元)' in czett:
                subscription_cz = float(subscription_cz)*10000
            elif '亿' in czett:
                subscription_cz = float(subscription_cz)*100000000
            elif '万美元' in czett:
                subscription_cz = float(subscription_cz)*10000*7.1
            # print("认缴出资额")
            print(subscription_cz,'        认缴出资额')
            # items[-1]['subscription_capital'] = int(subscription_cz)
            items[-1]['subscription_capital'] = subscription_cz


        return items



    #对新格式重新获取的函数fzNewInfo
    def fzNewInfo(self,response):

        # logging.warning('*'*100)


        items = []
        # print(items)

        # 公司名
        companyname = response.xpath('//div[@class="content"]/div[1]/h1/text()').extract_first().strip().replace('\n', '')
        print(companyname, '    公司名')

        # 统一社会信用代码
        creditnumber = response.xpath( '//section[@id="Cominfo"]/table[@class="ntable"]/tr[3]/td[2]/text()').extract_first().strip().replace('\n','')
        print(creditnumber, '    统一社会信用代码')

        # 得到股东信息表格的内容
        table_gd3 = response.xpath('//table[@class="ntable ntable-odd npth nptd"]')
        table_gdx1 = table_gd3[0]

        i = 0

        # 判断关于新格式中符合标准的内容在list中那个位置
        for title in table_gd3:
            tname = title.xpath('./tr[1]/th[3]/text()').extract_first()
            # print(tname)
            if tname == "持股比例":
                # ls_index = table_gd.index(tname)
                table_gdx1 = table_gd3[i]
                break
            i += 1

        gd_list1 = table_gdx1.xpath('./tr')
        print(len(gd_list1))


        #查看./td[4] 的标题
        print(gd_list1[0])
        gd_title = gd_list1[0]
        title4 = gd_title.xpath('./th[4]/span/text()').extract_first()
        print(title4 ,'   fzNewInfo')

        #如果 认缴出资额 在title4 中 那么就使用NewNewInfo 函数提取新格式的内容
        if title4 is not None:
            if '认缴出资额' in title4:
                items = self.NewNewInfo(gd_list1,title4,companyname,creditnumber)
                return items

        for gd in gd_list1[1:]:

            item = QichachaItem()

            item['company_name'] = companyname
            items.append(item)

            items[-1]['credit_number'] = creditnumber

            # 股东姓名
            shareholder_nm = gd.xpath('./td[2]/table/tr/td[2]/a/h3/text()').extract_first()

            if shareholder_nm == None:
                shareholder_nm = gd.xpath('./td[2]/table/tr/td[2]/div/a/h3/text()').extract_first()
                if shareholder_nm == None:
                    shareholder_nm = gd.xpath('./td[2]/table/tr/td[2]/div/h3/text()').extract_first()
            print(shareholder_nm,'   股东姓名')
            items[-1]['shareholder'] = shareholder_nm

            # 股份比例
            shareholding_bl = gd.xpath('./td[3]/text()').extract_first().strip()
            print(shareholding_bl,'      股份比例')
            items[-1]['shareholding_ratio'] = shareholding_bl

            # 持股数
            number_of_shares = gd.xpath('./td[4]/text()').extract_first().strip()
            number_of_shares = number_of_shares.replace(',', '')
            items[-1]['number_of_shares'] = number_of_shares
            print(number_of_shares,'        持股数')

        return items


    def NewNewInfo(self,gd_list1,title4,companyname,creditnumber):

        items= []
        print(title4 , 'NewNewInfo')

        for gd in gd_list1[1:]:

            item = QichachaItem()
            item['company_name'] = companyname
            items.append(item)

            items[-1]['credit_number'] = creditnumber


            # 股东姓名
            shareholder_nm = gd.xpath('./td[2]/table/tr/td[2]/a/h3/text()').extract_first()
            if shareholder_nm == None:
                shareholder_nm = gd.xpath('./td[2]/table/tr/td[2]/div/a/h3/text()').extract_first()
                if shareholder_nm == None:
                    shareholder_nm = gd.xpath('./td[2]/table/tr/td[2]/div/h3/text()').extract_first()
            print(shareholder_nm,'       股东姓名')
            items[-1]['shareholder'] = shareholder_nm

            # 股份比例
            shareholding_bl = gd.xpath('./td[3]/text()').extract_first().strip()
            print(shareholding_bl,'        股份比例')
            items[-1]['shareholding_ratio'] = shareholding_bl

            # 认缴出资日期
            subscription_dt = gd.xpath('./td[5]/text()').extract_first().strip('\t\n\r ,')
            print(subscription_dt,'           认缴出资日期')
            items[-1]['subscription_date'] = subscription_dt

            # 认缴出资额
            subscription_cz = gd.xpath('./td[4]/text()').extract_first().strip('\t\n\r ,')
            # number_of_shares = number_of_shares.replace(',', '')
            if subscription_cz == '-':
                # subscription_cz = 0

                subscription_cz = 0

            if '(万元)' in title4:
                subscription_cz = float(subscription_cz) * 10000
            elif '亿' in title4:
                subscription_cz = float(subscription_cz) * 100000000
            elif '万美元' in title4:
                subscription_cz = float(subscription_cz) * 10000 * 7.1
                # print("认缴出资额")
            print(subscription_cz,'            认缴出资额')
            # items[-1]['subscription_capital'] = int(subscription_cz)
            items[-1]['subscription_capital'] = subscription_cz

        return items
