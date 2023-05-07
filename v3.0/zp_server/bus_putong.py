from flask import Blueprint,request,jsonify
from data.mysqlHelper import get_a_conn
from bus_cloud import GetWordCloud
from zhongweishu import median
 
putong_api = Blueprint('putong_api', __name__)

# 公司性质
@putong_api.route('/getComXz', methods=['POST'])
def getComXz():
    mysql = get_a_conn()
    sql = "SELECT companytype_text value,companytype_text label from tbl_job WHERE companytype_text is not null and companytype_text != '' GROUP BY companytype_text  "
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})

# 公司规模
@putong_api.route('/getComSize', methods=['POST'])
def getComSize():
    mysql = get_a_conn()
    sql = "SELECT company_size value,company_size label from tbl_job WHERE company_size is not null and company_size != '' GROUP BY company_size "
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})

# 所有城市查询
@putong_api.route('/citysTs', methods=['POST'])
def citysTs():
    mysql = get_a_conn()
    sql = "select DISTINCT provinceid value,provinceid label from tbl_job_canji union all "
    sql += "select DISTINCT cityid value,cityid label from tbl_job_canji union all "
    sql += "select DISTINCT three_cityid value,three_cityid label from tbl_job_canji "
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})

# 薪资预测
@putong_api.route('/yuce', methods=['POST'])
def yuce():
    try:
        search = request.json.get('search', None)
        location = request.json.get('location', None)
        xueli = request.json.get('xueli', None)
        jingyan = request.json.get('jingyan', None)
        company = request.json.get('company', None)
        companytype_text = request.json.get('companytype_text', None)
        mysql = get_a_conn()
        sql = "SELECT ( t.a + t.b ) / 2 avg0 FROM ( " \
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
              "	salary,search,xueli,location FROM ( " \
              "		SELECT substring_index( salary, '·13薪', 1 ) AS q,SUBSTRING_INDEX( salary, '-', 1 ) a,SUBSTRING_INDEX( salary, '-',- 1 ) b,salary,search,xueli,location  FROM tbl_job  WHERE 1 = 1  "
        if search != None and search != '' and search != 'undefined':
            sql += " and (job_name like '%"
            sql += search
            sql += " %' or search like '%"
            sql += search
            sql += "%')"
        if xueli != None and xueli != '' and xueli != 'undefined':
            sql += " and xueli = '%s'" % (xueli)
        if location != None and location != '' and location != 'undefined':
            sql += " and location like '%"
            sql += location
            sql += "%' "
        if jingyan != None and jingyan != '' and jingyan != 'undefined':
            sql += " and jingyan = '%s'" % (jingyan)
        if company != None and company != '' and company != 'undefined':
            sql += " and company_size = '%s'" % (company)
        if companytype_text != None and companytype_text != '' and companytype_text != 'undefined':
            sql += " and companytype_text = '%s'" % (companytype_text)
        sql += " ) x) t"

        print(sql)
        result = mysql.fetchall(sql)
        res = '0'
        if result:
            xinziList = ''
            for avg in result:
                xinziList += str(avg.get('avg0'))
                xinziList += ','
            res = median(list(eval(xinziList)))
        return jsonify({'code': '200', 'info': res})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})

# 推荐职位
@putong_api.route('/zwtj', methods=['POST'])
def zwtj():
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

    sql = "SELECT *,(SELECT count(1) FROM tbl_user_job WHERE job_id = t.id and user_id = " + str(user_id) + ") is_collect FROM tbl_job t WHERE 1=1 "
    if search != None and search != '':
        sql += " and (job_name like '%"
        sql += search
        sql += " %' or search like '%"
        sql += search
        sql += "%') "
    if exp != None and exp != '' and exp != 'undefined':
        sql += " and GetNumber(jingyan, 0) <= '%s' " % (exp)
    if xueli != None and xueli != '' and xueli != 'undefined':
        if xueli == '硕士':
            sql += " and xueli in ('硕士','本科','大专','中技/中专','高中','初中及以下','学历不限','None','') "
        if xueli == '本科':
            sql += " and xueli in ('本科','大专','中技/中专','高中','初中及以下','学历不限','None','') "
        if xueli == '大专':
            sql += " and xueli in ('大专','中技/中专','高中','初中及以下','学历不限','None','') "
        if xueli == '中技/中专':
            sql += " and xueli in ('中技/中专','高中','初中及以下','学历不限','None','') "
        if xueli == '高中':
            sql += " and xueli in ('中技/中专','高中','初中及以下','学历不限','None','') "
        if xueli == '初中及以下':
            sql += " and xueli in ('初中及以下','学历不限','None','') "
    if location != None and location != '':
        sql += "and location like '%"
        sql += location
        sql += "%' "
    sql += " ORDER BY create_time desc limit %s,%s" % ((pageno - 1) * pagesize, pagesize)
    result = mysql.fetchall(sql)
    sql_count = 'select count(1) num from tbl_job  WHERE 1=1 '
    if search != None and search != '':
        sql_count += " and (job_name like '%"
        sql_count += search
        sql_count += " %' or search like '%"
        sql_count += search
        sql_count += "%') "
    if exp != None and exp != '' and exp != 'undefined':
        sql_count += " and GetNumber(jingyan, 0) <= '%s' " % (exp)
    if xueli != None and xueli != '' and xueli != 'undefined':
        if xueli == '硕士':
            sql_count += " and xueli in ('硕士','本科','大专','中技/中专','高中','初中及以下','学历不限','None','') "
        if xueli == '本科':
            sql_count += " and xueli in ('本科','大专','中技/中专','高中','初中及以下','学历不限','None','') "
        if xueli == '大专':
            sql_count += " and xueli in ('大专','中技/中专','高中','初中及以下','学历不限','None','') "
        if xueli == '中技/中专':
            sql_count += " and xueli in ('中技/中专','高中','初中及以下','学历不限','None','') "
        if xueli == '高中':
            sql_count += " and xueli in ('中技/中专','高中','初中及以下','学历不限','None','') "
        if xueli == '初中及以下':
            sql_count += " and xueli in ('初中及以下','学历不限','None','') "
    if location != None and location != '':
        sql_count += "and location like '%"
        sql_count += location
        sql_count += "%' "
    count = mysql.fetchall(sql_count)
    total = count[0].get('num')
    return jsonify({'code': '200', 'info': result, 'pageno': pageno, 'pagesize': pagesize, 'total': total})

# 公司信息分析
@putong_api.route('/gsinfo', methods=['POST'])
def gsinfo():
    try:
        type = request.form.get('type', None)
        search = request.form.get('search', None)
        location = request.form.get('location', None)
        xueli = request.form.get('xueli', None)
        mysql = get_a_conn()
        if type == 'sx':  # 公司属性
            sql = "SELECT company_sx name,count(company_sx) value FROM tbl_job where 1=1 "
        if type == "xz":  # 公司性质
            sql = "SELECT companytype_text name,count(companytype_text) value FROM tbl_job where 1=1 "
        if type == 'size':  # 公司规模
            sql = "SELECT company_size name,count(company_size) value FROM tbl_job where 1=1 "

        if search != None and search != '':
            sql += " and search = '%s'" % (search)
        if location != None and location != '':
            sql += " and location like '%"
            sql += location
            sql += "%' "
        if xueli != None and xueli != '':
            sql += " and xueli = '%s'" % (xueli)

        if type == 'sx':  # 公司属性
            sql += "GROUP BY company_sx ORDER BY count(company_sx) desc limit 15 "
        if type == "xz":  # 公司性质
            sql += "GROUP BY companytype_text ORDER BY count(companytype_text) desc "
        if type == 'size':  # 公司规模
            sql += "GROUP BY company_size ORDER BY count(company_size) desc "
        result = mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': result, 'type': type})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 生成福利词云
@putong_api.route('/fuli', methods=['POST'])
def fuli():
    search = request.json.get('search', None)
    location = request.json.get('location', None)
    xueli = request.json.get('xueli', None)
    jingyan = request.json.get('jingyan', None)
    short_evals = ""
    mysql = get_a_conn()
    sql = "SELECT fuli FROM tbl_job WHERE fuli != ''"
    if search != None and search != '' and search != 'undefined':
        sql += " and (job_name like '%"
        sql += search
        sql += " %' or search like '%"
        sql += search
        sql += "%')"
    if xueli != None and xueli != '' and xueli != 'undefined':
        sql += " and xueli = '%s'" % (xueli)
    if location != None and location != '' and location != 'undefined':
        sql += " and location like '%"
        sql += location
        sql += "%' "
    if jingyan != None and jingyan != '' and jingyan != 'undefined':
        sql += " and jingyan = '%s'" % (jingyan)
    evals = mysql.fetchall(sql)
    if (len(evals) > 0):
        for item in evals:
            short_evals += item.get('fuli')
    else:
        short_evals += '暂无数据'
    result = GetWordCloud(short_evals)
    if result == '1':
        return jsonify({'code': '200', 'info': '生成词云图成功'})
    else:
        return jsonify({'code': '500', 'info': '生成词云图失败'})


# 经验要求
@putong_api.route('/jingyan', methods=['POST'])
def jingyan():
    mysql = get_a_conn()
    sql = "SELECT jingyan value,jingyan label FROM tbl_job GROUP BY jingyan"
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})


# 学历要求
@putong_api.route('/xueli', methods=['POST'])
def xueli():
    mysql = get_a_conn()
    sql = "SELECT xueli value,xueli label FROM tbl_job GROUP BY xueli"
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})


# 招聘要求
@putong_api.route('/yaoqiu', methods=['POST'])
def yaoqiu():
    search = request.form.get('search', None)
    location = request.form.get('location', None)
    mysql = get_a_conn()
    sql_jingyan = "SELECT jingyan name,count(jingyan) value FROM tbl_job where 1=1  "
    sql_xueli = "SELECT xueli name,count(xueli) value FROM tbl_job where 1=1  "
    if search != None and search != '':
        sql_jingyan += " and search = '%s'" % (search)
        sql_xueli += " and search = '%s'" % (search)
    if location != None and location != '':
        sql_jingyan += " and location like '%"
        sql_jingyan += location
        sql_jingyan += "%' "
        sql_xueli += " and location like '%"
        sql_xueli += location
        sql_xueli += "%' "
    sql_jingyan += "GROUP BY jingyan"
    sql_xueli += "GROUP BY xueli"
    result_jingyan = mysql.fetchall(sql_jingyan)
    result_xueli = mysql.fetchall(sql_xueli)
    return jsonify({'code': '200', 'info': result_jingyan, 'info2': result_xueli})


# 薪资比例
@putong_api.route('/zpXinzi', methods=['POST'])
def zpXinzi():
    search = request.form.get('search', None)
    xueli = request.form.get('xueli', None)
    location = request.form.get('location', None)
    mysql = get_a_conn()
    sql = "SELECT z.xinzi name,count(z.xinzi) value from (  " \
          "	SELECT case when (y.a+y.b)/2 < 5000 then '小于5千元'" \
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
          "	salary,search,xueli,location FROM ( " \
          "		SELECT substring_index( salary, '·13薪', 1 ) AS q,SUBSTRING_INDEX( salary, '-', 1 ) a,SUBSTRING_INDEX( salary, '-',- 1 ) b,salary,search,xueli,location  FROM tbl_job  " \
          "  where 1=1 "
    if search != None and search != '':
        sql += " and search = '%s'" % (search)
    if xueli != None and xueli != '':
        sql += " and xueli = '%s'" % (xueli)
    if location != None and location != '':
        sql += " and location like '%"
        sql += location
        sql += "%' "
    sql += " ) x) y) z GROUP BY z.xinzi "
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})

# 职位招聘分析
@putong_api.route('/jobTop', methods=['POST'])
def jobTop():
    xueli = request.json.get('xueli', None)
    location = request.json.get('location', None)
    mysql = get_a_conn()
    sql = 'select job_name name ,count(job_name) value FROM tbl_job  WHERE 1=1 '
    if xueli != None and xueli != '':
        sql += " and xueli = '%s'" % (xueli)
    if location != None and location != '':
        sql += " and location like '%"
        sql += location
        sql += "%' "
    sql += "GROUP BY job_name ORDER BY count(job_name) desc limit 30 "
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})

# 城市招聘分布
@putong_api.route('/zpcity', methods=['POST'])
def zpcity():
    search = request.form.get('search', None)
    mysql = get_a_conn()
    sql = 'SELECT t.location name,count(t.location) value FROM tbl_job t  WHERE 1=1 '
    if search != None and search != '':
        sql += " and search = '%s'" % (search)
    sql += " group by t.location ORDER BY count(t.location) desc limit 30 "
    result = mysql.fetchall(sql)
    return jsonify({'code': '200', 'info': result})

# 删除
@putong_api.route('/delData', methods=['POST'])
def delData():
    try:
        id = request.form.get('id')
        if (id == None or id == '' or id == 'undefined'):
            return jsonify({'code': '500', 'info': 'id不存在，删除失败'})
        mysql = get_a_conn()
        sql = "delete from tbl_job where id =  '%s'" % id
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '删除成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': '删除失败' + e})

# 数据概览
@putong_api.route('/getDatas', methods=['POST'])
def getDatas():
    pageno = int(request.json.get('pageNo', 1))
    pagesize = int(request.json.get('pageSize', 10))
    search = request.json.get('search', None)
    location = request.json.get('location', None)
    xueli = request.json.get('xueli', None)
    user_id = request.json.get('user_id')
    searchType = request.json.get('searchType')
    mysql = get_a_conn()
    sql = "SELECT *,(SELECT count(1) FROM tbl_user_job WHERE job_id = t.id and user_id = " + str(user_id) + ") is_collect FROM tbl_job t WHERE 1=1 "
    if search != None and search != '':
        sql += " and (job_name like '%"
        sql += search
        sql += " %' or search like '%"
        sql += search
        sql += "%') "
    if xueli != None and xueli != '':
        sql += " and xueli = '%s'" % (xueli)
    if location != None and location != '':
        sql += " and location like '%"
        sql += location
        sql += "%' "
    if searchType != None and searchType != '' and searchType == '0':
        sql += " and (SELECT count(1) FROM tbl_user_job WHERE job_id = t.id and user_id = " + str(user_id) + ")  > 0 "
    sql += " ORDER BY create_time desc limit %s,%s" % ((pageno - 1) * pagesize, pagesize)
    result = mysql.fetchall(sql)
    sql_count = 'select count(1) num from tbl_job  t WHERE 1=1 '
    if search != None and search != '':
        sql_count += " and (job_name like '%"
        sql_count += search
        sql_count += " %' or search like '%"
        sql_count += search
        sql_count += "%') "
    if xueli != None and xueli != '':
        sql_count += " and xueli = '%s'" % (xueli)
    if location != None and location != '':
        sql_count += " and location like '%"
        sql_count += location
        sql_count += "%' "
    if searchType != None and searchType != '' and searchType == '0':
        sql_count += " and (SELECT count(1) FROM tbl_user_job WHERE job_id = t.id and user_id = " + str(user_id) + ")  > 0 "
    count = mysql.fetchall(sql_count)
    total = count[0].get('num')
    return jsonify({'code': '200', 'info': result, 'pageno': pageno, 'pagesize': pagesize, 'total': total})