from data.mysqlHelper import get_a_conn


# 保存日志
def saveLog(user_name, start_time, end_time, data_num, data_url, data_mode, detail, state):
    mysql = get_a_conn()
    sql = 'insert into tbl_data_log (user_name,start_time,end_time,data_num,data_url,data_mode,detail,state) values ("%s","%s","%s","%s","%s","%s","%s","%s")' % (
        user_name, start_time, end_time, data_num, data_url, data_mode, detail, state)
    mysql.execute(sql)
