from flask import Blueprint,request,jsonify
from data.mysqlHelper import get_a_conn
from data.data_zhilian import getZhilian
 
index_api = Blueprint('index_api', __name__)

# 51job城市字典表
@index_api.route('/getCityDict', methods=['POST'])
def getCityDict():
    try:
        mysql = get_a_conn()
        sql = "select city_code value,city_name label from tbl_city"
        res = mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': res})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})

# 取消收藏
@index_api.route('/delCollect', methods=['POST'])
def delCollect():
    try:
        user_id = request.json.get('user_id')
        job_id = int(request.json.get('job_id'))
        mysql = get_a_conn()
        sql = "delete from tbl_user_job where user_id = '%s' and job_id = '%s'" % (user_id, job_id)
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '取消成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})

# 收藏
@index_api.route('/collect', methods=['POST'])
def collect():
    try:
        user_id = request.json.get('user_id')
        job_id = int(request.json.get('job_id'))
        mysql = get_a_conn()
        sql = "insert into tbl_user_job (user_id,job_id) values (%s,%s) " % (user_id, job_id)
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '新增成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})

# 获取日志
@index_api.route('/getLogs', methods=['POST'])
def getLogs():
    pageno = int(request.json.get('pageNo', 1))
    pagesize = int(request.json.get('pageSize', 10))
    userRole = request.json.get('userRole')
    userName = request.json.get('userName')
    mysql = get_a_conn()
    sql = "SELECT * FROM tbl_data_log where 1=1 "
    if userRole != None and userRole != '' and userRole != '1':
        sql += "and user_name = '"  + str(userName) + "'"
    sql += "ORDER BY end_time desc limit %s,%s" % ((pageno - 1) * pagesize, pagesize)
    result = mysql.fetchall(sql)
    sql_count = 'select count(1) num from tbl_data_log where 1=1 '
    if userRole != None and userRole != '' and userRole != '1':
        sql_count += "and user_name = '"  + str(userName) + "'"
    count = mysql.fetchall(sql_count)
    total = count[0].get('num')
    return jsonify({'code': '200', 'info': result, 'pageno': pageno, 'pagesize': pagesize, 'total': total})


# 爬取数据
@index_api.route('/getJobData', methods=['POST'])
def getJobs():
    username = request.json.get('username')
    search = request.json.get('search', '+')
    pagesize = int(request.json.get('pageSize', 2))
    city_id = request.json.get('city_id', 358)
    if search == '':
        search = ''
    if city_id == '':
        city_id = 358
    result = getZhilian(username,city_id, search, pagesize)
    return jsonify({'code': '200', 'info': result})


# 用户新增
@index_api.route('/addUser', methods=['POST'])
def addUser():
    try:
        account = request.json.get('account')
        name = request.json.get('name')
        email = request.json.get('email')
        phone = request.json.get('phone')
        role = request.json.get('role')
        remarks = request.json.get('remarks')
        mysql = get_a_conn()
        sql = "insert into tbl_user (name,account,pwd,email,phone,login_flag,remarks,role) values ('%s','%s','%s','%s','%s','%s','%s','%s') " % (
            name, account, '123456', email, phone, '1', remarks, role)
        mysql.fetchall(sql)

        return jsonify({'code': '200', 'info': '新增成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})

# 用户信息
@index_api.route('/userInfo', methods=['POST'])
def userInfo():
    account = request.form.get("account")
    mysql = get_a_conn()
    sql = "SELECT * FROM tbl_user where 1=1 "
    if account != None and account != '':
        sql += " and account = '"
        sql += account
        sql += "'"
    result = mysql.fetchall(sql)
    sql_count = 'select count(1) num from tbl_user'
    count = mysql.fetchall(sql_count)
    total = count[0].get('num')
    return jsonify({'code': '200', 'info': result})


# 用户编辑
@index_api.route('/editUser', methods=['POST'])
def editUser():
    try:
        print(request.form)

        print('=============')
        print(request.json)
        id = request.json.get('id')
        name = request.json.get('name')
        email = request.json.get('email')
        phone = request.json.get('phone')
        role = request.json.get('role')
        remarks = request.json.get('remarks')
        icon = request.json.get('img')
        location = '' if (request.json.get('location') == 'None' or request.json.get('location') == None) else request.json.get('location')
        exp = '' if request.json.get('exp') == 'None' else request.json.get('exp')
        deu = '' if request.json.get('deu') == 'None' else request.json.get('deu')
        major = '' if request.json.get('major') == 'None' else request.json.get('major')
        mysql = get_a_conn()
        sql = "update tbl_user set name = '%s',email='%s',phone='%s',role='%s',remarks='%s',location='%s',exp='%s',deu='%s',major='%s',img='%s' where id = '%s'" % (
            name, email, phone, role, remarks,location,exp,deu,major, icon,id)
        mysql.fetchall(sql)

        return jsonify({'code': '200', 'info': '修改成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 用户停用
@index_api.route('/stopUser', methods=['POST'])
def stopUser():
    try:
        id = request.form.get('id')
        if (id == None or id == '' or id == 'undefined'):
            return jsonify({'code': '500', 'info': 'id不存在，启用失败'})
        mysql = get_a_conn()
        sql = "update tbl_user set login_flag = '0' where id = '%s'" % id
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '停用成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 重置密码
@index_api.route('/chongzhi', methods=['POST'])
def chongzhi():
    try:
        id = request.form.get('id')
        if (id == None or id == '' or id == 'undefined'):
            return jsonify({'code': '500', 'info': 'id不存在，重置失败'})
        mysql = get_a_conn()
        sql = "update tbl_user set pwd = '123456' where id = '%s'" % id
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '重置成功，密码为 123456'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 用户启用
@index_api.route('/startUser', methods=['POST'])
def startUser():
    try:
        id = request.form.get('id')
        if (id == None or id == '' or id == 'undefined'):
            return jsonify({'code': '500', 'info': 'id不存在，启用失败'})
        mysql = get_a_conn()
        sql = "update tbl_user set login_flag = '1' where id = '%s'" % id
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '启用成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 用户删除
@index_api.route('/delUser', methods=['POST'])
def delUser():
    try:
        id = request.form.get('id')
        if (id == None or id == '' or id == 'undefined'):
            return jsonify({'code': '500', 'info': 'id不存在，删除失败'})
        mysql = get_a_conn()
        sql = "delete from tbl_user where id =  '%s'" % id
        mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '删除成功'})
    except Exception as e:
        return jsonify({'code': '500', 'info': '删除失败' + e})


# 用户列表
@index_api.route('/getUsers', methods=['POST'])
def getUsers():
    pageno = int(request.form.get('pageNo', 1))
    pagesize = int(request.form.get('pageSize', 10))
    name = request.form.get("name")
    phone = request.form.get("phone")
    mysql = get_a_conn()
    sql = "SELECT * FROM tbl_user where 1=1 "
    if name != None and name != '':
        sql += " and name like '%"
        sql += name
        sql += "%'"
    if phone != None and phone != '':
        sql += " and phone = '%s'" % (phone)
    sql += " ORDER BY id asc limit %s,%s" % ((pageno - 1) * pagesize, pagesize)
    result = mysql.fetchall(sql)
    sql_count = 'select count(1) num from tbl_user'
    count = mysql.fetchall(sql_count)
    total = count[0].get('num')
    return jsonify({'code': '200', 'info': result, 'pageno': pageno, 'pagesize': pagesize, 'total': total})


# 修改密码
@index_api.route('/changePwd', methods=['POST'])
def changePwd():
    account = request.form.get('account', None)
    oldPwd = request.form.get('oldPwd', None)
    newPwd = request.form.get('newPwd', None)
    mysql = get_a_conn()
    sql = """ SELECT * FROM tbl_user t where t.account = '%s' and t.pwd = '%s' """ % (account, oldPwd)
    result = mysql.fetchall(sql)
    if (result):
        sql = "update tbl_user set pwd = '%s' WHERE account = '%s'" % (newPwd, account)
        result1 = mysql.fetchall(sql)
        print(result1)
        return jsonify({'code': '200', 'info': '修改成功'})
    else:
        return jsonify({'code': '500', 'info': '旧密码输入不正确'})


# 注册
@index_api.route('/reg', methods=['POST'])
def reg():
    try:
        account = request.form.get('account', None)
        pwd = request.form.get('pwd', None)
        name = request.form.get('name', None)
        role = request.form.get('role', None)

        # 账号是否存在校验
        mysql = get_a_conn()
        sql_username = 'select count(1) count from tbl_user t where t.account = "%s"' % (account)
        result = mysql.fetchall(sql_username)
        if (result[0].get('count') > 0):
            return jsonify({'code': '500', 'info': '该账号已注册'})
        else:
            sql = "INSERT into tbl_user (name,account,pwd,login_flag,role) values ('%s','%s','%s','%s','%s')" % (
                name, account, pwd, '1', role)
            mysql = get_a_conn()
            mysql.fetchall(sql)
        return jsonify({'code': '200', 'info': '注册成功，请登录'})
    except Exception as e:
        return jsonify({'code': '500', 'info': e})


# 登录
@index_api.route('/login', methods=['POST'])
def login():
    account = request.form.get('account', None)
    pwd = request.form.get('pwd', None)
    mysql = get_a_conn()
    sql = """ SELECT * FROM tbl_user t where t.account = '%s' and t.pwd = '%s' """ % (account, pwd)
    result = mysql.fetchall(sql)
    if (result):
        return {'code': '200', 'info': '%s登录成功' % account, 'session':result}
    else:
        return {'code': '500', 'info': '%s登录失败' % account}