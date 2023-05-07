from flask import Blueprint,request,jsonify
from data.mysqlHelper import get_a_conn
from bus_cloud import GetWordCloud
from zhongweishu import median

teshu_api = Blueprint('teshu_api', __name__)

# 薪资预测
@teshu_api.route('/yuceTs', methods=['POST'])
def yuceTs():
    try:
        search = request.json.get('search', None)
        location = request.json.get('location', None)
        xueli = request.json.get('xueli', None)
        jingyan = request.json.get('jingyan', None)
        company = request.json.get('company', None)
        companytype_text = request.json.get('companytype_text', None)
        mysql = get_a_conn()
        # TODO 计算中位数
        sql = "SELECT ( t.a + t.b ) / 2 avg0 FROM ( " \
               "SELECT q, " \
              "	case when a like '%千'  then a*1000  " \
              "		 when a like '%千' or a like '%千及以下'  then a*1000  " \
              "		 when a not like '%千' and a not like '%万' and b like '%万' then a*10000 " \
              "		 when a not like '%千' and a not like '%万' and b like '%千' then a*1000 " \
              "		 when a not like '%千' and a not like '%万' and (b like '%万·13薪' or b like '%万·14薪')then a*10000 " \
              "		 when a not like '%千' and a not like '%万' and b like '%万/年' then  round(a*10000/12,0) " \
              "		 else 0 end as a, " \
              "	case when b like '%千'  then b*1000  " \
              "		 when b like '%千' or a like '%千及以下'  then b*1000  " \
              "		 when b like '%万' then b*10000 " \
              "		 when b like '%万·13薪' or b like '%万·14薪' then b*10000 " \
              "		 when b like '%万/年' then  round(b*10000/12,0) " \
              "		 else 0 end as b, " \
              "	salary,search,edu,exp,provinceid,cityid,three_cityid FROM (  " \
              "		SELECT substring_index( job_salary, '·13薪', 1 ) AS q,SUBSTRING_INDEX( job_salary, '-', 1 ) a,SUBSTRING_INDEX( job_salary, '-',- 1 ) b,job_salary salary,search,edu,exp,provinceid,cityid,three_cityid  FROM tbl_job_canji " \
              "  where 1=1 "
        if search != None and search != '' and search != 'undefined':
            sql += " and (job_name like '%"
            sql += search
            sql += "%' or search like '%"
            sql += search
            sql += "%') "
        if location != None and location != '' and location != 'undefined':
            sql += " and (provinceid like '%"
            sql += location
            sql += "%' or cityid like '%"
            sql += location
            sql += "%' or three_cityid like '%"
            sql += location
            sql += "%') "
        if xueli != None and xueli != '' and xueli != 'undefined':
            sql += " and edu = '%s'" % (xueli)
        if jingyan != None and jingyan != '' and jingyan != 'undefined':
            sql += " and exp = '%s'" % (jingyan)
        if company != None and company != '' and company != 'undefined':
            sql += " and mun = '%s'" % (company)
        if companytype_text != None and companytype_text != '' and companytype_text != 'undefined':
            sql += " and pr = '%s'" % (companytype_text)
        sql += " ) x where (x.a != 0 and x.b !=0) ) t"
        result = mysql.fetchall(sql)
        zws = '0'
        if result:
            xinziList = ''
            for avg in result:
                xinziList += str(avg.get('avg0'))
                xinziList += ','
            zws = median(list(eval(xinziList)))

        # TODO 计算平均、最大、最小
        sql2 = "SELECT ROUND(avg((a+b)/2),2) avg ,min(t.a) min,max(b) max FROM ( " \
               "SELECT q, " \
               "	case when a like '%千'  then a*1000  " \
               "		 when a like '%千' or a like '%千及以下'  then a*1000  " \
               "		 when a not like '%千' and a not like '%万' and b like '%万' then a*10000 " \
               "		 when a not like '%千' and a not like '%万' and b like '%千' then a*1000 " \
               "		 when a not like '%千' and a not like '%万' and (b like '%万·13薪' or b like '%万·14薪')then a*10000 " \
               "		 when a not like '%千' and a not like '%万' and b like '%万/年' then  round(a*10000/12,0) " \
               "		 else 0 end as a, " \
               "	case when b like '%千'  then b*1000  " \
               "		 when b like '%千' or a like '%千及以下'  then b*1000  " \
               "		 when b like '%万' then b*10000 " \
               "		 when b like '%万·13薪' or b like '%万·14薪' then b*10000 " \
               "		 when b like '%万/年' then  round(b*10000/12,0) " \
               "		 else 0 end as b, " \
               "	salary,search,edu,exp,provinceid,cityid,three_cityid FROM (  " \
               "		SELECT substring_index( job_salary, '·13薪', 1 ) AS q,SUBSTRING_INDEX( job_salary, '-', 1 ) a,SUBSTRING_INDEX( job_salary, '-',- 1 ) b,job_salary salary,search,edu,exp,provinceid,cityid,three_cityid  FROM tbl_job_canji " \
               "  where 1=1 "
        if search != None and search != '' and search != 'undefined':
            sql2 += " and (job_name like '%"
            sql2 += search
            sql2 += "%' or search like '%"
            sql2 += search
            sql2 += "%') "
        if location != None and location != '' and location != 'undefined':
            sql2 += " and (provinceid like '%"
            sql2 += location
            sql2 += "%' or cityid like '%"
            sql2 += location
            sql2 += "%' or three_cityid like '%"
            sql2 += location
            sql2 += "%') "
        if xueli != None and xueli != '' and xueli != 'undefined':
            sql2 += " and edu = '%s'" % (xueli)
        if jingyan != None and jingyan != '' and jingyan != 'undefined':
            sql2 += " and exp = '%s'" % (jingyan)
        if company != None and company != '' and company != 'undefined':
            sql2 += " and mun = '%s'" % (company)
        if companytype_text != None and companytype_text != '' and companytype_text != 'undefined':
            sql2 += " and pr = '%s'" % (companytype_text)
        sql2 += " ) x where (x.a != 0 and x.b !=0) ) t where t.a > 0"
        res = mysql.fetchall(sql2)
        return jsonify({'code': '200', 'info': zws, 'info2': res})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})

# 所有城市查询
@teshu_api.route('/citysTs', methods=['POST'])
def citysTs():
    mysql = get_a_conn()
    sql = "select DISTINCT provinceid value,provinceid label from tbl_job_canji union all "
    sql += "select DISTINCT cityid value,cityid label from tbl_job_canji union all "
    sql += "select DISTINCT three_cityid value,three_cityid label from tbl_job_canji "
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})

# 职位推荐
@teshu_api.route('/zwtjTs', methods=['POST'])
def zwtjTs():
    mysql = get_a_conn()
    account = request.json.get('account', None)
    pageno = int(request.json.get('pageNo', 1))
    pagesize = int(request.json.get('pageSize', 10))
    user_id = request.json.get('user_id')

    user_sql = 'select * from tbl_user where account = "%s"' % account
    user_info = mysql.fetchall(user_sql)
    exp = user_info[0].get('exp')
    location = user_info[0].get('location')
    xueli = user_info[0].get('deu')
    search = user_info[0].get('major')
    if (exp == '' or exp == None or exp == 'null') and (location == '' or location == None or location == 'null') and(xueli == '' or xueli == None or xueli == 'null') and(search == '' or search == None or search == 'null') :
        return jsonify({'code': '500', 'info': '请完善个人信息'})
    sql = "SELECT * ,(SELECT count(1) FROM tbl_user_job WHERE job_id = t.job_id and user_id = " + str(user_id) + ") is_collect FROM tbl_job_canji t WHERE 1=1"
    if search != None and search != '':
        sql += " and (job_name like '%"
        sql += search
        sql += "%' or search like '%"
        sql += search
        sql += "%') "
    if xueli != None and xueli != '' and xueli != 'undefined':
        if xueli == '硕士':
            sql += " and edu in ('硕士','本科','大专','高中/中专','初中','小学','学历不限','None','') "
        if xueli == '本科':
            sql += " and edu in ('本科','大专','高中/中专','初中','小学','学历不限','None','') "
        if xueli == '大专':
            sql += " and edu in ('大专','高中/中专','初中','小学','学历不限','None','') "
        if xueli == '高中/中专':
            sql += " and edu in ('高中/中专','初中','小学','学历不限','None','') "
        if xueli == '初中':
            sql += " and edu in ('初中','小学','学历不限','None','') "
        if xueli == '小学':
            sql += " and edu in ('小学','学历不限','None','') "
    if exp != None and exp != '' and exp != 'undefined' and exp != '99':
        sql += " and GetNumber(exp, 0) <= '%s' and exp != '应届毕业生' " % (exp)
    if exp == '99':
        sql += " and exp = '应届毕业生' "
    if location != None and location != '':
        sql += " and (provinceid like '%"
        sql += location
        sql += "%' or cityid like '%"
        sql += location
        sql += "%' or three_cityid like '%"
        sql += location
        sql += "%') "
    sql += " ORDER BY create_time desc limit %s,%s" % ((pageno - 1) * pagesize, pagesize)
    result = mysql.fetchall(sql)
    sql_count = 'select count(1) num from tbl_job_canji  WHERE 1=1 '
    if search != None and search != '':
        sql_count += " and (job_name like '%"
        sql_count += search
        sql_count += "%' or search like '%"
        sql_count += search
        sql_count += "%') "
    if xueli != None and xueli != '' and xueli != 'undefined':
        if xueli == '硕士' :
            sql_count += " and edu in ('硕士','本科','大专','高中/中专','初中','小学','学历不限','None','') "
        if xueli == '本科' :
            sql_count += " and edu in ('本科','大专','高中/中专','初中','小学','学历不限','None','') "
        if xueli == '大专' :
            sql_count += " and edu in ('大专','高中/中专','初中','小学','学历不限','None','') "
        if xueli == '高中/中专' :
            sql_count += " and edu in ('高中/中专','初中','小学','学历不限','None','') "
        if xueli == '初中' :
            sql_count += " and edu in ('初中','小学','学历不限','None','') "
        if xueli == '小学' :
            sql_count += " and edu in ('小学','学历不限','None','') "
    if exp != None and exp != '' and exp != 'undefined' and exp != '99':
        sql_count += " and GetNumber(exp, 0) <= '%s' and exp != '应届毕业生' " % (exp)
    if exp == '99':
        sql_count += " and exp = '应届毕业生' "
    if location != None and location != '':
        sql_count += " and (provinceid like '%"
        sql_count += location
        sql_count += "%' or cityid like '%"
        sql_count += location
        sql_count += "%' or three_cityid like '%"
        sql_count += location
        sql_count += "%') "
    count = mysql.fetchall(sql_count)
    total = count[0].get('num')
    return jsonify({'code': '200', 'info': result, 'pageno': pageno, 'pagesize': pagesize, 'total': total})


# 公司信息分析
@teshu_api.route('/gsinfoTs', methods=['POST'])
def gsinfoTs():
    try:
        type = request.json.get('type', None)
        search = request.json.get('search', None)
        location = request.json.get('location', None)
        xueli = request.json.get('xueli', None)
        exp = request.json.get('exp', None)
        mysql = get_a_conn()
        if type == 'sx':  # 行业
            sql = "SELECT hy_top name,count(hy_top) value FROM tbl_job_canji where 1=1  "
        if type == "xz":  # 公司性质
            sql = "SELECT pr name,count(pr) value FROM tbl_job_canji where 1=1 AND pr is not null and pr != 'None' and pr != '' "
        if type == 'size':  # 公司规模
            sql = "SELECT mun name,count(mun) value FROM tbl_job_canji where 1=1 and mun != 'None' and mun != '' "

        if search != None and search != '' and search != 'undefined':
            sql += " and (job_name like '%"
            sql += search
            sql += "%' or search like '%"
            sql += search
            sql += "%') "
        if location != None and location != '' and location != 'undefined':
            sql += " and (provinceid like '%"
            sql += location
            sql += "%' or cityid like '%"
            sql += location
            sql += "%' or three_cityid like '%"
            sql += location
            sql += "%') "
        if xueli != None and xueli != '' and xueli != 'undefined':
            sql += " and edu = '%s'" % (xueli)
        if exp != None and exp != '' and exp !=  'undefined':
            sql += " and exp = '%s'" % (exp)

        if type == 'sx':  # 行业
            sql += "GROUP BY hy_top ORDER BY count(hy_top) desc "
        if type == "xz":  # 公司性质
            sql += "GROUP BY pr ORDER BY count(pr) desc  "
        if type == 'size':  # 公司规模
            sql += "GROUP BY mun ORDER BY count(mun) desc "
        result = mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': result, 'type': type})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})

# 招聘要求
@teshu_api.route('/yaoqiuTs', methods=['POST'])
def yaoqiuTs():
    search = request.form.get('search', None)
    location = request.form.get('location', None)
    mysql = get_a_conn()
    sql_jingyan = "SELECT exp as name,count(exp) as value FROM tbl_job_canji where exp is not null and exp != 'None'  "
    sql_xueli = "SELECT edu name,count(edu) value FROM tbl_job_canji where edu is not null and edu != 'None'  "
    if search != None and search != '':
        sql_jingyan += " and (job_name like '%"
        sql_jingyan += search
        sql_jingyan += "%' or search like '%"
        sql_jingyan += search
        sql_jingyan += "%') "

        sql_xueli += " and (job_name like '%"
        sql_xueli += search
        sql_xueli += "%' or search like '%"
        sql_xueli += search
        sql_xueli += "%') "
    if location != None and location != '':
        sql_jingyan += " and (provinceid like '%"
        sql_jingyan += location
        sql_jingyan += "%' or cityid like '%"
        sql_jingyan += location
        sql_jingyan += "%' or three_cityid like '%"
        sql_jingyan += location
        sql_jingyan += "%') "

        sql_xueli += " and (provinceid like '%"
        sql_xueli += location
        sql_xueli += "%' or cityid like '%"
        sql_xueli += location
        sql_xueli += "%' or three_cityid like '%"
        sql_xueli += location
        sql_xueli += "%') "
    sql_jingyan += "GROUP BY exp"
    sql_xueli += "GROUP BY edu"
    result_jingyan = mysql.fetchall(sql_jingyan)
    result_xueli = mysql.fetchall(sql_xueli)
    return jsonify({'code': '200', 'info': result_jingyan, 'info2': result_xueli})

# 薪资比例
@teshu_api.route('/zpXinziTs', methods=['POST'])
def zpXinziTs():
    search = request.json.get('search', None)
    xueli = request.json.get('xueli', None)
    location = request.json.get('location', None)
    exp = request.json.get('exp', None)
    mysql = get_a_conn()
    sql = "SELECT z.xinzi name,count(z.xinzi) value from (   " \
          "	SELECT case when salary = '面议' then '面议' when (y.a+y.b)/2 < 5000 then '小于5千元'" \
          "					when (y.a+y.b)/2 >= 5000 && (y.a+y.b)/2 < 10000 then '5千-1万元'" \
          "					when (y.a+y.b)/2 >= 10000 && (y.a+y.b)/2 < 15000 then '1万-1.5万元'  " \
          "					when (y.a+y.b)/2 >= 15000 && (y.a+y.b)/2 < 20000 then '1.5万-2万元'" \
          "					when (y.a+y.b)/2 >= 20000 && (y.a+y.b)/2 < 25000 then '2万-2.5万元'" \
          "					when (y.a+y.b)/2 >= 25000 && (y.a+y.b)/2 < 3000 then '2万-2.5万元'" \
          "					else '大于3万'" \
          "					end xinzi" \
          "	from (    " \
          "	SELECT q, " \
          "	case when a like '%千'  then a*1000  " \
          "		 when a like '%千' or a like '%千及以下'  then a*1000  " \
          "		 when a not like '%千' and a not like '%万' and b like '%万' then a*10000 " \
          "		 when a not like '%千' and a not like '%万' and b like '%千' then a*1000 " \
          "		 when a not like '%千' and a not like '%万' and (b like '%万·13薪' or b like '%万·14薪')then a*10000 " \
          "		 when a not like '%千' and a not like '%万' and b like '%万/年' then  round(a*10000/12,0) " \
          "		 else 0 end as a, " \
          "	case when b like '%千'  then b*1000  " \
          "		 when b like '%千' or a like '%千及以下'  then b*1000  " \
          "		 when b like '%万' then b*10000 " \
          "		 when b like '%万·13薪' or b like '%万·14薪' then b*10000 " \
          "		 when b like '%万/年' then  round(b*10000/12,0) " \
          "		 else 0 end as b, " \
          "	salary,search,edu,exp,provinceid,cityid,three_cityid FROM (  " \
          "		SELECT substring_index( job_salary, '·13薪', 1 ) AS q,SUBSTRING_INDEX( job_salary, '-', 1 ) a,SUBSTRING_INDEX( job_salary, '-',- 1 ) b,job_salary salary,search,edu,exp,provinceid,cityid,three_cityid  FROM tbl_job_canji " \
          "  where 1=1 "
    if search != None and search != '' and search != 'undefined':
        sql += " and (job_name like '%"
        sql += search
        sql += "%' or search like '%"
        sql += search
        sql += "%') "
    if location != None and location != '' and location != 'undefined':
        sql += " and (provinceid like '%"
        sql += location
        sql += "%' or cityid like '%"
        sql += location
        sql += "%' or three_cityid like '%"
        sql += location
        sql += "%') "
    if xueli != None and xueli != '' and xueli != 'undefined':
        sql += " and edu = '%s'" % (xueli)
    if exp != None and exp != '' and exp != 'undefined':
        sql += " and exp = '%s'" % (exp)
    sql += " ) x) y) z GROUP BY z.xinzi "
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})


# 生成标签词云
@teshu_api.route('/cloudTs', methods=['POST'])
def cloudTs():
    search = request.json.get('search', None)
    location = request.json.get('location', None)
    xueli = request.json.get('xueli', None)
    exp = request.json.get('exp', None)

    short_evals = ""
    mysql = get_a_conn()
    sql = "SELECT job_labels FROM tbl_job_canji WHERE job_labels != '' "
    if search != None and search != '' and search != 'undefined':
        sql += " and (job_name like '%"
        sql += search
        sql += "%' or search like '%"
        sql += search
        sql += "%') "
    if location != None and location != '' and location != 'undefined':
        sql += " and (provinceid like '%"
        sql += location
        sql += "%' or cityid like '%"
        sql += location
        sql += "%' or three_cityid like '%"
        sql += location
        sql += "%') "
    if xueli != None and xueli != '' and xueli != 'undefined':
        sql += " and edu = '%s'" % (xueli)
    if exp != None and exp != '' and exp != 'undefined':
        sql += " and exp = '%s'" % (exp)
    evals = mysql.fetchall(sql)
    if (len(evals) > 0):
        for item in evals:
            short_evals += item.get('job_labels')
    else:
        short_evals += '暂无数据'
    for item in evals:
        short_evals += item.get('job_labels')
    result = GetWordCloud(short_evals)
    if result == '1':
        return jsonify({'code': '200', 'info': '生成词云图成功'})
    else:
        return jsonify({'code': '500', 'info': '生成词云图失败'})

# 职位招聘分析
@teshu_api.route('/tsJobTop', methods=['POST'])
def tsJobTop():
    edu = request.json.get('edu', None)
    location = request.json.get('location', None)
    exp = request.json.get('exp', None)
    mysql = get_a_conn()
    sql = 'select job_name name ,count(job_name) value FROM tbl_job_canji  WHERE 1=1  '
    if edu != None and edu != '' and edu != 'undefined':
        sql += " and edu = '%s'" % (edu)
    if exp != None and exp != '' and exp != 'undefined':
        sql += " and exp = '%s'" % (exp)
    if location != None and location != '':
        sql += " and (provinceid like '%"
        sql += location
        sql += "%' or cityid like '%"
        sql += location
        sql += "%' or three_cityid like '%"
        sql += location
        sql += "%') "
    sql += " GROUP BY job_name ORDER BY count(job_name) desc limit 30"
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})

# 城市招聘分布
@teshu_api.route('/tszpcity', methods=['POST'])
def tszpcity():
    search = request.json.get('search', None)
    edu = request.json.get('edu', None)
    exp = request.json.get('exp', None)
    mysql = get_a_conn()
    if search != None and search != '' and search == '2':
        sql = 'SELECT t.cityid name,count(t.cityid) value FROM tbl_job_canji t  WHERE 1=1  '
        if edu != None and edu != '':
            sql += " and edu = '%s'" % (edu)
        if exp != None and exp != '':
            sql += " and exp = '%s'" % (exp)
        sql += " group by t.cityid ORDER BY count(t.cityid) desc limit 30 "
    if search != None and search != '' and search == '3':
        sql = 'SELECT t.three_cityid name,count(t.three_cityid) value FROM tbl_job_canji t  WHERE 1=1  '
        if edu != None and edu != '':
            sql += " and edu = '%s'" % (edu)
        if exp != None and exp != '':
            sql += " and exp = '%s'" % (exp)
        sql += " group by t.three_cityid ORDER BY count(t.three_cityid) desc limit 30 "
    if search == None or search == '' or search == '1' or search == 'undefined':
        sql = 'SELECT t.provinceid name,count(t.provinceid) value FROM tbl_job_canji t  WHERE 1=1  '
        if edu != None and edu != '':
            sql += " and edu = '%s'" % (edu)
        if exp != None and exp != '':
            sql += " and exp = '%s'" % (exp)
        sql += " group by t.provinceid ORDER BY count(t.provinceid) desc limit 30 "
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})

# 经验要求
@teshu_api.route('/tsjingyan', methods=['POST'])
def tsjingyan():
    mysql = get_a_conn()
    sql = "SELECT exp value,exp label FROM tbl_job_canji where exp != 'None' GROUP BY exp "
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})


# 学历要求
@teshu_api.route('/tsXueli', methods=['POST'])
def tsXueli():
    mysql = get_a_conn()
    sql = "SELECT edu value,edu label FROM tbl_job_canji WHERE edu != 'None' and edu is not null and edu != ''  GROUP BY edu"
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})

# 删除
@teshu_api.route('/delTsData', methods=['POST'])
def delTsData():
    try:
        id = request.form.get('id')
        if (id == None or id == '' or id == 'undefined'):
            return jsonify({'code': '500', 'info': 'id不存在，删除失败'})
        mysql = get_a_conn()
        sql = "delete from tbl_job_canji where job_id =  '%s'" % id
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '删除成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': '删除失败' + e})

# 数据概览
@teshu_api.route('/getTsDatas', methods=['POST'])
def getTsDatas():
    pageno = int(request.json.get('pageNo', 1))
    pagesize = int(request.json.get('pageSize', 10))
    search = request.json.get('search', None)
    location = request.json.get('location', None)
    xueli = request.json.get('xueli', None)
    exp = request.json.get('exp', None)
    user_id = request.json.get('user_id')
    searchType = request.json.get('searchType')
    mysql = get_a_conn()
    sql = "SELECT * ,(SELECT count(1) FROM tbl_user_job WHERE job_id = t.job_id and user_id = " + str(user_id) + ") is_collect FROM tbl_job_canji t WHERE 1=1"
    if search != None and search != '':
        sql += " and (job_name like '%"
        sql += search
        sql += "%' or search like '%"
        sql += search
        sql += "%') "
    if xueli != None and xueli != '' and xueli != 'undefined':
        sql += " and edu = '%s'" % (xueli)
    if exp != None and exp != '' and exp != 'undefined':
        sql += " and exp = '%s'" % (exp)
    if location != None and location != '':
        sql += " and (provinceid like '%"
        sql += location
        sql += "%' or cityid like '%"
        sql += location
        sql += "%' or three_cityid like '%"
        sql += location
        sql += "%') "
    if searchType != None and searchType != '' and searchType == '0':
        sql += " and (SELECT count(1) FROM tbl_user_job WHERE job_id = t.job_id and user_id = " + str(user_id) + ")  > 0 "
    sql += " ORDER BY create_time desc limit %s,%s" % ((pageno - 1) * pagesize, pagesize)
    result = mysql.fetchall(sql)
    sql_count = 'select count(1) num from tbl_job_canji t  WHERE 1=1 '
    if search != None and search != '':
        sql_count += " and (job_name like '%"
        sql_count += search
        sql_count += "%' or search like '%"
        sql_count += search
        sql_count += "%') "
    if xueli != None and xueli != '' and xueli != 'undefined':
        sql_count += " and edu = '%s'" % (xueli)
    if exp != None and exp != '' and exp != 'undefined':
        sql_count += " and exp = '%s'" % (exp)
    if location != None and location != '':
        sql_count += " and (provinceid like '%"
        sql_count += location
        sql_count += "%' or cityid like '%"
        sql_count += location
        sql_count += "%' or three_cityid like '%"
        sql_count += location
        sql_count += "%') "
    if searchType != None and searchType != '' and searchType == '0':
        sql_count += " and (SELECT count(1) FROM tbl_user_job WHERE job_id = t.job_id and user_id = " + str(user_id) + ")  > 0 "
    count = mysql.fetchall(sql_count)
    total = count[0].get('num')
    return jsonify({'code': '200', 'info': result, 'pageno': pageno, 'pagesize': pagesize, 'total': total})