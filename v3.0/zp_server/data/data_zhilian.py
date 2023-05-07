import requests
from bs4 import BeautifulSoup
import time
from data.mysqlHelper import get_a_conn
from data.data_log import saveLog
import datetime
import random

headers = {
    'authority': 'sou.zhaopin.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,und;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'cookie': 'FSSBBIl1UgzbN7NO=5Z1ufo8N4VNXT3fUeLPrpHfv3IZAstfZBODnmkdnmi.w.oe1dklX1QHIQfaCOb7nWeb7dJsN3vYOV4DGXzWCVWG; x-zp-client-id=d1c7c17e-006a-48ae-8c25-2d7f3474c947; locationInfo_search={%22code%22:%22768%22%2C%22name%22:%22%E4%BD%9B%E5%B1%B1%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1672143883; zp_passport_deepknow_sessionId=7326fc4ds3feab43cd924806c291fdbecf8f; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221054094145%22%2C%22first_id%22%3A%22185538aca737d5-03dc2e5a99cf8a-26021151-1327104-185538aca74e77%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg1NTM4YWNhNzM3ZDUtMDNkYzJlNWE5OWNmOGEtMjYwMjExNTEtMTMyNzEwNC0xODU1MzhhY2E3NGU3NyIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjEwNTQwOTQxNDUifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221054094145%22%7D%2C%22%24device_id%22%3A%22185538aca737d5-03dc2e5a99cf8a-26021151-1327104-185538aca74e77%22%7D; acw_tc=276077ca16724704540073351e1a423008eb76ef0551f36de11b1aaad19737; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1672470459; FSSBBIl1UgzbN7NP=53_dIXKiB64LqqqDmRaoSMaEIIb0i8UNvQjiNo3qnjBvMxW6sxR.FbdulAS1_9wI_dDekfOC_iisZOXLJKlKF3ES8oY_mzRfqTdEuE7yeLd7thd8116S87dT25ZjVityVIk1wczhlGQ1I7EJoM8F90wvKYQYH64L.RgiXKIdCrH4_pdE2LLzQGo75gzlX_7kyi6QrHMCaRPVdFXHhgyFEQxvkCxYUbN1hhfa5Wb2rugItZ1y9L8HYiE7MqcyTkAChjrrzGkK6cFW6WA5Y.v3j01G5doEAzjhMbaZv_GQcNNRUIEw_qpTmvEJ2CVPTI9fITapVmUDtQVTADAkNrrEO83',
    'referer': 'https://i.zhaopin.com/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

url = 'https://sou.zhaopin.com/?jl={}&kw={}&p={}'
url2 = 'https://sou.zhaopin.com/?jl={}&p={}'

def getZhilian(username,city,search,pageSize):
    data = []
    log = ''
    startTime = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S")
    try:

        log += '{} 开始爬取数据\n'.format(
                datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"))

        for page in range(1, pageSize+1):
            if search != '' and search != None :
                url_get = url.format(city,search,page)
            else :
                url_get = url2.format(city,page)
            log += '{} 第{}页 开始获取数据\n'.format(
                    datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"), page)
            log += '{} url:  {}\n'.format(
                    datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"), url_get)
            response = requests.get(url_get, headers=headers)
            soup = BeautifulSoup(response.text,'html.parser')
            job_div = soup.find('div', class_='positionlist')
            job_list = job_div.find_all('div',class_='joblist-box__item clearfix')
            log += '{} 第{}页 数据获取完毕，开始解析数据\n'.format(
                    datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"), page)
            print('{} 第{}页 数据获取完毕，开始解析数据\n'.format(
                    datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"), page))
            for job in job_list :
                # 详情链接
                job_href = job.find('a')['href']
                # 工作第一行
                line1 = job.find('div',class_='iteminfo__line iteminfo__line1')
                # 名字
                job_name_div = line1.find('div',class_='iteminfo__line1__jobname')
                job_name =job_name_div.find('span').text
                # 公司名字
                company_name_div = line1.find('div',class_='iteminfo__line1__compname')
                company_name = company_name_div.find('span').text

                # 工作第二行
                line2 = job.find('div',class_='iteminfo__line iteminfo__line2')
                line2_jobdesc = line2.find('div',class_='iteminfo__line2__jobdesc')
                # 薪资
                salary = line2_jobdesc.find('p').text.replace('\n','').replace(' ','')
                line2_jobdesc_ul = line2_jobdesc.find('ul')
                line2_jobdesc_li = line2_jobdesc_ul.find_all('li')
                # 工作地点
                location = ''
                # 经验
                jingyan = ''
                # 学历
                xueli = ''
                for i, line in enumerate(line2_jobdesc_li):
                    if i == 0:
                        location = line.text
                    if i == 1:
                        jingyan = line.text
                    if i == 2:
                        xueli = line.text
                line_comdesc = line2.find_all('span',class_='iteminfo__line2__compdesc__item')
                # 公司性质
                companytype_text = ''
                # 公司规模
                company_size = ''
                for i,line in enumerate(line_comdesc):
                    if i == 0:
                        companytype_text = line.text
                    if i == 1:
                        company_size = line.text

                # 工作第三行
                line3 = job.find('div',class_='iteminfo__line iteminfo__line3')
                line3__welfare = line3.find('div',class_='iteminfo__line3__welfare')
                line3__welfare_item = line3__welfare.find_all('div',class_='iteminfo__line3__welfare__item')
                fuli = ''
                for item in line3__welfare_item:
                    fuli =  fuli + ' ' + item.text
                # 状态
                pub_time = line3.find('div',class_='iteminfo__line3__status').text
                data.append({
                    "job_name": job_name,
                    "company": company_name,
                    "salary": salary,
                    "location": location,
                    "jingyan": jingyan,
                    "xueli": xueli,
                    "pub_time": pub_time,
                    "companytype_text": companytype_text,
                    "fuli": fuli,
                    "company_sx": '',
                    "company_size": company_size,
                    "job_href": job_href
                })
            log += '{} 第{}页 数据解析完毕\n'.format(
                    datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"), page)
            # 防止爬取过快
            time.sleep(random.randint(2, 5))
        #  数据入库
        mysql = get_a_conn()
        count_insert = 0
        count_update = 0
        for item in data:
            createTime = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S")
            # 判断 如果数据已存在，则更新，反之插入
            sqlSelect = 'select * from tbl_job where job_href = "%s"' % item['job_href']
            result = mysql.fetchall(sqlSelect)
            if (len(result) > 0):
                sql_update = "update tbl_job set job_name='%s',pub_time='%s',salary='%s',hangye='%s',company='%s'," \
                             "location='%s',jingyan='%s',xueli='%s',fuli='%s',company_sx='%s',company_size='%s'," \
                             "companytype_text='%s',company_href='%s',create_time='%s',create_user='%s'," \
                             "search='%s' " \
                             "where job_href = '%s'" \
                      % (item.get('job_name'),item.get('pub_time'),item.get('salary'),item.get(''),item.get('company'),item.get('location'),item.get('jingyan'),
                           item.get('xueli'),item.get('fuli'),item.get('company_sx'),item.get('company_size'),item.get('companytype_text'),'',
                           createTime,username,search,item.get('job_href'))
                mysql.fetchall(sql_update)
                count_update+=1
            else:
                sqlInsrt = 'INSERT INTO tbl_job (job_name,pub_time,salary,hangye,company,location,jingyan,xueli,fuli,company_sx,company_size,companytype_text,company_href,job_href,create_time,create_user,search) ' \
                       'VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'\
                       %  (item.get('job_name'),item.get('pub_time'),item.get('salary'),item.get(''),item.get('company'),item.get('location'),item.get('jingyan'),
                           item.get('xueli'),item.get('fuli'),item.get('company_sx'),item.get('company_size'),item.get('companytype_text'),'',
                           item.get('job_href'),createTime,username,search)
                mysql.fetchall(sqlInsrt)
                count_insert+=1
        log += '{} 数据入库完毕\n'.format(
            datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"))
        log += '{} 成功！ 新增{}条数据，更新{}条数据\n'.format(datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"),count_insert,count_update)
        print("================ 数据入库完毕,新增{}条数据，更新{}条数据 ".format(count_insert,count_update))
        # 插入日志
        endTime = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S")
        saveLog(username, startTime, endTime, str(len(data)), url_get, search, log, '1')
        return log
    except Exception as e:
        print('失败：')
        print(e)
        log += '{} 失败：{}\n'.format(datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S"),e)
        # 插入日志
        endTime = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S")
        saveLog(username, startTime, endTime, str(len(data)), url_get, search , log, '0')
        return log

if __name__ == '__main__':
    result = getZhilian("后台",358,'java',1)

