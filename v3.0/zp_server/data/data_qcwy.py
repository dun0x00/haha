import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,und;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'From-Domain': '51job_web',
    'Origin': 'https://we.51job.com',
    'Referer': 'https://we.51job.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'account-id': '144593812',
    'partner': 'www_baidu_com',
    'property': '%7B%22partner%22%3A%22www_baidu_com%22%2C%22webId%22%3A2%2C%22fromdomain%22%3A%2251job_web%22%2C%22frompageUrl%22%3A%22https%3A%2F%2Fwe.51job.com%2F%22%2C%22pageUrl%22%3A%22https%3A%2F%2Fwe.51job.com%2Fpc%2Fsearch%3Fkeyword%3Dphp%22%2C%22identityType%22%3A%22%E8%81%8C%E5%9C%BA%E4%BA%BA%22%2C%22userType%22%3A%22%E8%80%81%E7%94%A8%E6%88%B7%22%2C%22isLogin%22%3A%22%E6%98%AF%22%2C%22accountid%22%3A%22144593812%22%7D',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sign': '5c9e8218cd9eaf9fbba538296c882c8229b828f9bfe4c30b3d0280cdec8df90b',
    'user-token': 'f8f195ce57a655a952a53b5ab308ba1f63a69c1c',
    'uuid': 'a884b8253c2f5a48b2923e4aaeca56e9',
}

params = {
    'api_key': '51job',
    'timestamp': '1671865400',
    'keyword': 'php',
    'searchType': '2',
    'function': '',
    'industry': '',
    'jobArea': '000000',
    'jobArea2': '',
    'landmark': '',
    'metro': '',
    'salary': '',
    'workYear': '',
    'degree': '',
    'companyType': '',
    'companySize': '',
    'jobType': '',
    'issueDate': '',
    'sortType': '0',
    'pageNum': '2',
    'requestId': '8f9048fe6ab692eb24b847fbd81dbd37',
    'pageSize': '50',
    'source': '1',
    'accountId': '144593812',
    'pageCode': 'sou|sou|soulb',
}

response = requests.get('https://cupid.51job.com/open/noauth/search-pc', params=params, headers=headers)
json_data = response.json()
print(json_data)
status = json_data['status']
job_data = json_data['resultbody']['job']['items']
for job in job_data:
    labels = ''
    if len(job['jobTags']) >0 :
            for item in job['jobTags']:
                labels += item + ' '
    data_param = {
        # 岗位id
        'jobId': job['jobId'],
        # 岗位名称
        'job_name': job['jobName'],
        # 发布时间
        'pub_time': job['updateDateTime'],
        # 薪资
        'salary': job['provideSalaryString'],
        # 类型
        'hangye': job['industryType1Str'],
        # 公司名称
        'company': job['companyName'],
        # 工作地点
        'location': job['jobAreaString'],
        # 经验
        'jingyan': job['workYearString'],
        # 学历
        'xueli': job['degreeString'],
        # 标签
        'fuli': labels,
        # 公司属性
        'company_sx': job['industryType2Str'],
        # 公司规模
        'company_size': job['companySizeString'],
        # 公司性质
        'companytype_text': job['companyTypeString'],
        # 公司详情页地址
        'company_href': job['companyHref'],
        # 招聘详情页地址
        'job_href': job['jobHref']

    }
    print(data_param)

print(job_data)