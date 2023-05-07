import requests
import time

headers = {
    'authority': 'www.zhipin.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,und;q=0.8,en;q=0.7',
    'cookie': 'sid=sem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1671862566; wd_guid=fcb4460d-f54e-4d6d-a1ce-2e1589b44513; historyState=state; _bl_uid=h3lUhcwp1vUjqnt8j46q288eph6F; wt2=DXFKZRbMeh6-_S1MvM61hLlbdW-b9yC8SmWSVPbmdTB3Ya9crskE0yT0zEA5RSiTra4G0BqD9G_xjM-4yj2zo3w~~; wbg=0; __g=sem_pz_bdpc_dasou_title; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1671885494; __zp_stoken__=cdcfeNCEvOQxkUjgFTig5MUwjZy5BYDxyC3pxFXYMQ2k7c3wpPX51d3cfPQtQGn9ta3RIXHQpPj0hRnpiaAtQKikZNUoCewlnLgwkcH4mRF02JQZ%2Bcy55T30cBk8tcAQSAQIiO0AcAl5reBpgE3cMQBBEBE5AQjsGdXdUDUE8NA%3D%3D; __c=1671862566; __l=l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3Djava%26city%3D100010000&r=https%3A%2F%2Fwww.baidu.com%2Fother.php%3Fsc.Ks0000jgRV3cJL0heNiblfvKvlgWwb0ehXpix-AaiayLtJAS1Ckzol_LU5Dg-mANOq_rb3_4AfqOI-YWibw7g73jxsLhN7fwyK11GaI9c4YXfkI_--p48MqmwbUmQQ2gX6F-q_G9orAchufQDe5TypudzDqWaWZQ_Ud7p1p4loSCmcydssnVQ5mNklAcOW7ifTbiaWFLMxIYRtcLC8mW-jWiRX4w.7D_NR2Ar5Od663rj6t8AGSPticrtXFBPrM-kt5QxIW94UhmLmry6S9wiGyAp7BEIu80.TLFWgv-b5HDkrfK1ThPGujYknHb0THY0IAYqmhq1Tqpkko60IgP-T-qYXgK-5H00mywxIZ-suHY10ZIEThfqmhq1Tqpkko60ThPv5H00IgF_gv-b5HDdPjD1PjT4nWm0UgNxpyfqnHRsPWRYnWc0UNqGujYknH64njcsn0KVIZK_gv-b5HDzrjcv0ZKvgv-b5H00pywW5R9affKspyfqnHD0mv-b5Hcdr0KWThnqn1TsnHT%26dt%3D1671866416%26wd%3Dboss%25E7%259B%25B4%25E8%2581%2598%26tpl%3Dtpl_12826_30685_0%26l%3D1541347926%26us%3DlinkVersion%253D1%2526compPath%253D10036.0-10032.0%2526label%253D%2525E4%2525B8%2525BB%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkType%253D%2526linkText%253DBOSS%2525E7%25259B%2525B4%2525E8%252581%252598%2525E2%252580%252594%2525E2%252580%252594%2525E6%252589%2525BE%2525E5%2525B7%2525A5%2525E4%2525BD%25259C%2525EF%2525BC%25258C%2525E4%2525B8%25258ABOSS%2525E7%25259B%2525B4%2525E8%252581%252598%2525EF%2525BC%25258C&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&s=3&friend_source=0&s=3&friend_source=0; __a=17517544.1671862566..1671862566.21.1.21.21; geek_zp_token=V1RdMgF-3-3lpgXdNuzhUQLyq47zjTzA~~',
    'referer': 'https://www.zhipin.com/web/geek/job?query=java&city=100010000',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'token': 'sGkow6tHJclprSf',
    'traceid': '532CB4D0-6A8E-4200-9EAB-7B89E027D9BD',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'zp_token': 'V1RdMgF-3-3lpgXdNuzhUQLS-w5TnXwg~~',
}

url = 'https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query={}&city={}&page={}&pageSize=30'

# boss爬虫，cookie刷新时间太短，弃用

def getBoss(username,search,city,pageSize):
    try:
        for page in range(1, pageSize+1):
            print(url.format(search,city,page))
            response = requests.get(url.format(search,city,page),  headers=headers)
            json_data = response.json()
            code = json_data['code']
            print(code)
            jobList = json_data['zpData']['jobList']
            for job in jobList:
                labels = ''
                if len(job['welfareList']) >0 :
                    for item in job['welfareList']:
                        labels += item + ' '
                data_param = {
                    # 岗位id
                    'jobId': job['encryptJobId'],
                    # 岗位名称
                    'job_name': job['jobName'],
                    # 发布时间
                    # 'pub_time': job['updateDateTime'],
                    # 薪资
                    'salary': job['salaryDesc'],
                    # 类型
                    'hangye': job['brandIndustry'],
                    # 公司名称
                    'company': job['brandName'],
                    # 工作地点
                    'location': job['cityName'] + ' ' + job['areaDistrict'] + ' ' + job['businessDistrict'],
                    # 经验
                    'jingyan': job['jobExperience'],
                    # 学历
                    'xueli': job['jobDegree'],
                    # 标签
                    'fuli': labels,
                    # 公司属性
                    'company_sx': job['brandIndustry'],
                    # 公司规模
                    'company_size': job['brandScaleName'],
                    # 公司性质
                    'companytype_text': job['brandStageName'],
                    # 公司详情页地址
                    # 'company_href': job['companyHref'],
                    # 招聘详情页地址
                    # 'job_href': job['jobHref']

                }
                print(data_param)

            # 延时3秒
            time.sleep(3)
    except Exception as e:
        print('失败：')
        print(e)
        return '0'

if __name__ == '__main__':
    result = getBoss("后台",'java',100010000,10)