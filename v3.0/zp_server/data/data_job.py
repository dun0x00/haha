import urllib.parse
import random
import requests
from lxml import etree
import re
import json
import xlwt
import time
from data.mysqlHelper import get_a_conn
from data.data_log import saveLog
import datetime


class QianChengWuYouSpider(object):
    # 初始化
    def __init__(self,username, city_id, job_type, pages):
        # url模板
        self.url = 'https://search.51job.com/list/{},000000,0000,00,9,99,{},2,{}.html'
        # UA池
        self.UApool = [
            "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
            "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
            "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
            "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
        ]

        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            # 注意加上自己的Cookie
            'Cookie': 'SECKEY_ABVK=uAHDbzf1g/rU6AmiJsXT8YNQuXcittwzkzXVMmsqEwI%3D; BMAP_SECKEY=HTKdoozqrWpIIZ7QqdoJXmR35OqaYLlSkuqDrfSX201RerJY9_EX2F4l4b1FW3DlsZZ22zqrqasnRrlVb6K7L3q877GWT-C7hRMv_Zqa3Zz7oFJPxqXFsqHq6zo06c4ztJdYNYxEncKhsM5VUf_w5VFx8cSS-PzKyLBBUPJ61Qik0DnsGgzQomJ9GtDdf9Ng; guid=a884b8253c2f5a48b2923e4aaeca56e9; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; ps=needv%3D0; sensor=createDate%3D2018-08-22%26%7C%26identityType%3D1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22144593812%22%2C%22first_id%22%3A%22183da368128b71-09b037101559d4-26021f51-2073600-183da368129b67%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgzZGEzNjgxMjhiNzEtMDliMDM3MTAxNTU5ZDQtMjYwMjFmNTEtMjA3MzYwMC0xODNkYTM2ODEyOWI2NyIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjE0NDU5MzgxMiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22144593812%22%7D%2C%22%24device_id%22%3A%22183da368128b71-09b037101559d4-26021f51-2073600-183da368129b67%22%7D; search=jobarea%7E%60000000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%7B%7D%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAjava%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAc%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch3%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAphp%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch4%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; 51job=cuid%3D144593812%26%7C%26cusername%3D7FJZtgATET4NWF6ESdJl%252B4cfUjdSJSeDAc5jzQs%252F6%252FQ%253D%26%7C%26cpassword%3D%26%7C%26cname%3DLf1Axe89rgwTerZU4SD7Fw%253D%253D%26%7C%26cemail%3D6sdThUGUWdDgC0V019r4O%252BGBMKa5OcwpZMQgWSO%252FGyg%253D%26%7C%26cemailstatus%3D0%26%7C%26cnickname%3D%26%7C%26ccry%3D.0zlAvPpz%252FYrE%26%7C%26cconfirmkey%3DzhBo5jVEg8OhE%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3DzhNLMjqGmfwCo%26%7C%26to%3D152005c80ae479191e1b619c572d6ef363a05897%26%7C%26; partner=localhost; slife=lastlogindate%3D20221223%26%7C%26; acw_tc=ac11000116718081432493728e00e112a3c962477d09c68eb0fe8daff89572; ssxmod_itna=Yq+OBKAK0Ie0hmDzxAhYoLq2xG2=ipCi3gQrD0HmeGzDAxn40iDtoPTgo=n=mlgi3GDIxqGCS6STvaokzChfI10Yx0aDbqGke5YOheDxaq0rD74irDDxD3cD7PGmDimC2D7O1lSyHHKGRD0YDzqDgD7QDVqDfDDLcR7htFwUjQeiexGt+AwD4FqDMD7tD/3hbEeDBQPctnwUtVeGWbEQ4oeGuDG6Ppkdex0PyBut2Ip53boeof8D5mYhaY+wwAAq+FG4oY3hwzBATm7wPCivwYAfdWXODG8h0/+GqeD=; ssxmod_itna2=Yq+OBKAK0Ie0hmDzxAhYoLq2xG2=ipCi3gmDnKf2b5DsqiDLiiNnSRoqmwlrtGOlokrUzeSiQy4Ot84LFXsKYSuP08rzFGvb4Zm4wocsDNikQhCt1Fe7bm9CcTAq74NkvEi3UtdjAuK03v0upeA23exeKObfjeVxtLKl2CCmIHfxU1COR+RRf=PPusfmn8GnbhbfY3+j2WNe9xpZadrQoMz6I+Rc3F6+EapxGFfOHw5nawpaA+5lvHh/EvLohKE9UvOn83aIWf=6g0w/RwqH9mivDGUeUxljn/b3E4m5t4ixG2YBD5SWCtDFAxitRV47fY7Mtb5D4DFqD+EItCw1mi4AIQBE/m2qAoygiMmrGD3S=PmBU9gExe01iNV=biYD',
        }

        # 请求参数
        self.params = {
            "lang": "c",
            "postchannel": 0000,
            "workyear": 99,
            "cotype": 99,
            "degreefrom": 99,
            "jobterm": 99,
            "companysize": 99,
            "ord_field": 0,
            "dibiaoid": 0,
            "line": '',
            "welfare": ''
        }

        # 日志
        self.log = ''

        # 保存的文件名
        self.filename = "前程无忧网" + job_type + "职位信息.xls"

        self.username = username

        # 城市编号
        self.city_id = city_id

        # 职位名称 【转为urlencode编码】
        self.job_type = urllib.parse.quote(job_type)

        # 页数
        self.pages = pages

        # 临时存储容器
        self.words = []

    # 请求网页
    def parse(self, url):
        response = requests.get(url=url, headers=self.headers, params=self.params)

        # 设置编码格式为gbk
        response.encoding = 'gbk'

        # 网页源代码
        return response.text

    # 数据提取
    def get_job(self, page_text):
        # xpath
        tree = etree.HTML(page_text)
        job_label = tree.xpath('//script[@type="text/javascript"]')[2].text

        # 正则表达式
        job_str = re.findall('"engine_jds":(.*"adid":""}]),', job_label)[0]

        # 转换为json类型
        data = json.loads(job_str)

        # 数据提取
        for item in data:
            # 职位名称
            job_name = item['job_name']

            # 职位链接
            job_href = item['job_href']

            # 公司名称
            company_name = item['company_name']

            # 公司链接
            company_href = item['company_href']

            # 月薪范围
            salary = item['providesalary_text']

            # 工作地点
            address = item['workarea_text']

            # 其他信息
            info_list = item['attribute_text']

            # 有个别数据不完整, 直接跳过
            if len(info_list) < 3:
                continue

            # 经验要求
            experience = info_list[1]

            # 学历要求
            education = info_list[2]

            # 发布日期
            update_date = item['updatedate']

            # 公司性质
            company_type = item['companytype_text']

            # 公司福利
            job_welf = item['jobwelf']

            # 公司行业
            company_status = item['companyind_text']

            # 公司规模
            company_size = item['companysize_text']

            self.words.append({
                "job_name": job_name,
                "company": company_name,
                "salary": salary,
                "location": address,
                "jingyan": experience,
                "xueli": education,
                "pub_time": update_date,
                "companytype_text": company_type,
                "fuli": job_welf,
                "company_sx": company_status,
                "company_size": company_size,
                "job_href": job_href,
                "company_href": company_href,
            })

        print("该页爬取完成")

    # 数据保存_xlsx
    def save_xlsx(self, words, filename, sheet_name='sheet1'):
        try:
            # 1、创建工作薄
            work_book = xlwt.Workbook(encoding='utf-8')
            # 2、创建sheet表单
            sheet = work_book.add_sheet(sheet_name)
            # 3、写表头
            head = []
            for k in words[0].keys():
                head.append(k)

            for i in range(len(head)):
                sheet.write(0, i, head[i])
            # 4、添加内容
            # 行号
            i = 1
            for item in words:
                for j in range(len(head)):
                    sheet.write(i, j, item[head[j]])
                # 写完一行，将行号+1
                i += 1
            # 保存
            work_book.save(filename)
            print('数据保存成功')

        except Exception as e:
            print('数据保存失败', e)


    def save_mysql(self, words, filename, sheet_name='sheet1'):
        try:
            mysql = get_a_conn()
            # sql = "delete from tbl_job where search = '%s'" % (self.job_type)
            # result = mysql.fetchall(sql)
            # print("--> 清除历史数据完成！")

            print("数据入库开始！")
            self.log += '{} 爬虫完毕，数据入库开始\n'.format(
                datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"))
            for item in words:
                # 数据入库
                createTime = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S")
                sqlInsrt = 'INSERT INTO tbl_job (job_name,pub_time,salary,hangye,company,location,jingyan,xueli,fuli,company_sx,company_size,companytype_text,company_href,job_href,create_time,create_user,search) ' \
                           'VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'\
                           %  (item.get('job_name'),item.get('pub_time'),item.get('salary'),item.get(''),item.get('company'),item.get('location'),item.get('jingyan'),
                               item.get('xueli'),item.get('fuli'),item.get('company_sx'),item.get('company_size'),item.get('companytype_text'),item.get('company_href'),
                               item.get('job_href'),createTime,self.username,self.job_type)
                mysql.fetchall(sqlInsrt)

            print("数据入库完毕！")
            self.log += '{} 数据入库完毕\n'.format(
                datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"))

        except Exception as e:
            print('数据保存失败', e)

    # 主程序
    def run(self):
        try:
            startTime = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S")
            self.log += '{} 开始爬取数据\n'.format(
                datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"))
            for page in range(1, self.pages + 1):
                # 拼接每页url
                url = self.url.format(self.city_id, self.job_type, page)

                # 请求网页
                page_text = self.parse(url)

                self.log += '{} 第{}页 请求网页成功\n'.format(
                    datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"), page)
                self.log += '{} url:{}\n'.format(
                    datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"), url)

                # 数据提取
                self.get_job(page_text)

                self.log += '{} 第{}页 数据提取成功\n'.format(
                    datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"),page)

                # 防止爬取过快
                time.sleep(random.randint(1, 2))

            self.save_mysql(words=self.words, filename=self.filename)


            self.log += '{} 成功！共获取到{}条数据\n'.format(datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"),len(self.words))
            # 插入日志
            endTime = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S")
            saveLog(self.username, startTime, endTime, str(len(self.words)), self.url, self.job_type+' '+str(self.city_id), self.log, '1')
            return self.log
        except Exception as e:
            print(e)
            self.log += '{} 失败：{}\n'.format(datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"),e)
            # 插入日志
            endTime = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S")
            saveLog(self.username, startTime, endTime, str(len(self.words)), self.url, self.job_type+' '+str(self.city_id), self.log, '0')
            return self.log


if __name__ == '__main__':
    # 实例化爬虫对象 全国爬虫职位信息
    # city_id：城市编号（tbl_city 表中有数据，尽量使用默认000000（全国））
    # job_type：职位名称 （尽量精准，爬取到的数据会更贴切,不要重复爬取同一个关键词）
    # pages：页数（自己指定，注意不要超过总页数）！！！为了防止爬取过多ip被封，尽量一次一两页这样爬取
    spider = QianChengWuYouSpider(username = '后台' ,city_id=000000, job_type="java", pages=2)

    # 运行主程序
    reslut = spider.run()
    print(reslut)

