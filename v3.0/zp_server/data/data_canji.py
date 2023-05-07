import requests
import time
from mysqlHelper import get_a_conn
import datetime

# TODO Cookie需要定时更换
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,und;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'Path=/; Path=/; Path=/; Hm_lvt_ee31947220a83dbba5919eb6c496b632=1670915292; Hm_lpvt_ee31947220a83dbba5919eb6c496b632=1670915292; SECKEY_ABVK=69EabyAYzRGl60/BzSzVfckjLg3b7q2B00wmRAZTsFg%3D; BMAP_SECKEY=E2j3Bl6wXdm9kTlZNIc2xQEPBfDDEDsuJo5Hc0-_IxxOtOa4Qwsv1Q-e4uUxqK26IKnFpbg95eTD5nnUEi3tgNJSXSjozKDPwL_lJYysDOvhb9skhfMc2ozOnWOfVBQZe5n64UZIAn_tdvDMEa9JvbcFFRd5tSSr3vAwNRoWdFiDzWwhB9jBsAlgz2cXgfkV',
    'Pragma': 'no-cache',
    'Referer': 'https://www.cdpee.org.cn/job/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

# https://www.cdpee.org.cn/job/
def getJobData(username,pageSize):
    # 数据爬取目标地址
    url = 'https://www.cdpee.org.cn/api/app-jycy-job/querySearchJobInfo?pageNum={}&pageSize=10'
    try:
        data_list = []
        # 数据清洗
        for page in range(1, pageSize+1):
            print("================ 第{}页数据 开始爬取".format(page))
            r = requests.get(url.format(page), headers=headers)
            json_data = r.json()['data']['records']
            if len(json_data) > 0:
                for data in json_data:
                    labels = ''
                    if len(data['jobLabels']) >0 :
                        for item in data['jobLabels']:
                            labels += item['labelName'] + ' '
                    data_param = {
                        # 岗位id
                        'id': data['id'],
                        # 岗位名称
                        'jobName': data['jobName'],
                        # 发布时间
                        'updateTime': data['updateTime'],
                        # 薪资
                        'jobSalary': data['jobSalary'],
                        # 类型
                        'jobTop': data['jobTop'],
                        # 公司名称
                        'companyName': data['companyInfo']['companyName'],
                        # 省
                        'provinceid': data['provinceid'],
                        # 市
                        'cityid': data['cityid'],
                        # 县
                        'threeCityid': data['threeCityid'],
                        # 经验
                        'exp': data['exp'],
                        # 学历
                        'edu': data['edu'],
                        # 标签
                        'jobLabels': labels,
                        # 行业
                        'hyTop': data['companyInfo']['hyTop'],
                        # 公司规模
                        'mun': data['companyInfo']['mun'],
                        # 公司性质
                        'pr': data['companyInfo']['pr'],
                        # 公司id
                        'companyInfo_id': data['companyInfo']['id'],
                        # 开始时间
                        'beginTime': data['beginTime'],
                        # 结束时间
                        'endTime': data['endTime']

                    }
                    data_list.append(data_param)
            else :
                print("================ 第{}页数据 暂无".format(page))
                break
            print("================ 第{}页数据 爬取完毕".format(page))
            # 延时3秒
            time.sleep(3)
        print("================ 爬取完毕，共获取到{}条数据".format(len(data_list)))

        # 数据入库
        print("================ 数据入库开始 ")
        createTime = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + time.strftime("%H:%M:%S")
        mysql = get_a_conn()
        count_insert = 0
        count_update = 0
        for data in data_list:
            # 判断 如果数据已存在，则更新，反之插入
            sqlSelect = 'select * from tbl_job_canji where job_id = "%s"' % data['id']
            result = mysql.fetchall(sqlSelect)
            if (len(result) > 0):
                sql_update = "update tbl_job_canji set job_name='%s',update_time='%s',job_salary='%s',job_top='%s',company_name='%s'," \
                             "provinceid='%s',cityid='%s',three_cityid='%s',exp='%s',edu='%s',job_labels='%s'," \
                             "hy_top='%s',mun='%s',pr='%s',companyInfo_id='%s'," \
                             "begin_time='%s',end_time='%s',create_time='%s',create_user='%s',search='%s' " \
                             "where job_id = '%s'" \
                      % (data['jobName'],data['updateTime'],data['jobSalary'],data['jobTop'],data['companyName'],
                              data['provinceid'],data['cityid'],data['threeCityid'],data['exp'],data['edu'],data['jobLabels'],
                              data['hyTop'],data['mun'],data['pr'],data['companyInfo_id'],
                              data['beginTime'],data['endTime'],createTime,username,'',data['id'])
                mysql.fetchall(sql_update)
                count_update+=1
            else:
                sql_insert = 'INSERT INTO tbl_job_canji (job_id,job_name,update_time,job_salary,job_top,company_name,' \
                           'provinceid,cityid,three_cityid,exp,edu,job_labels,hy_top,mun,pr,companyInfo_id,' \
                           'begin_time,end_time,create_time,create_user,search) ' \
                           'VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' \
                           % (data['id'],data['jobName'],data['updateTime'],data['jobSalary'],data['jobTop'],data['companyName'],
                              data['provinceid'],data['cityid'],data['threeCityid'],data['exp'],data['edu'],data['jobLabels'],
                              data['hyTop'],data['mun'],data['pr'],data['companyInfo_id'],
                              data['beginTime'],data['endTime'],createTime,username,'')
                mysql.fetchall(sql_insert)
                count_insert+=1
        print("================ 数据入库完毕,新增{}条数据，更新{}条数据 ".format(count_insert,count_update))


    except Exception as e:
        print('失败：')
        print(e)
        return '0'

if __name__ == '__main__':
    result = getJobData("脚本录入",1)
