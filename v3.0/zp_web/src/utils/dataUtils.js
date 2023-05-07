/**
 * 时间函数工具类
 */
export const dataUtils = {
  // 其他时间格式转为时间戳
  getTime: (time) => {
    return new Date(time).getTime()
  },
  //  时间戳转(yyyy-MM-dd)
  getLocalTime: (time) => {
    const date = new Date(time)
    const y = date.getFullYear()
    let M = date.getMonth() + 1
    M = M < 10 ? ('0' + M) : M
    let d = date.getDate()
    d = d < 10 ? ('0' + d) : d
    return y + '-' + M + '-' + d + ' '
  },
  //  时间戳转精确时间(yyyy-MM-dd HH:mm:ss)
  getExactTime: (time) => {
    const date = new Date(time)
    const y = date.getFullYear()
    let M = date.getMonth() + 1
    M = M < 10 ? ('0' + M) : M
    let d = date.getDate()
    d = d < 10 ? ('0' + d) : d
    let h = date.getHours()
    h = h < 10 ? ('0' + h) : h
    let m = date.getMinutes()
    m = m < 10 ? ('0' + m) : m
    let s = date.getSeconds()
    s = s < 10 ? ('0' + s) : s
    return y + '-' + M + '-' + d + ' ' + h + ':' + m + ':' + s
  },
  //兼容苹果浏览器safari的方法
  getExactTimeWithSafari: (time) => {
    //取得浏览器的userAgent字符串
    var userAgent = navigator.userAgent;
    //判断是否Safari浏览器
    if (userAgent.indexOf("Safari") > -1) {
      time = time.replace(/\-/g,"/");  //把'-'转成'/' yyyy/mm/dd
    }
    var date=new Date(time);
    var year=date.getFullYear();
    /* 在日期格式中，月份是从0开始的，因此要加0
     * 使用三元表达式在小于10的前面加0，以达到格式统一  如 09:11:05
     * */
    var month= date.getMonth()+1<10 ? "0"+(date.getMonth()+1) : date.getMonth()+1;
    var day=date.getDate()<10 ? "0"+date.getDate() : date.getDate();
    var hour=date.getHours()<10 ? "0"+date.getHours() : date.getHours();
    var minute=date.getMinutes()<10 ? "0"+date.getMinutes() : date.getMinutes();
    var second=date.getSeconds()<10 ? "0"+date.getSeconds() : date.getSeconds();
    return year+"-"+month+"-"+day+" "+hour+":"+minute+":"+second;
  },
  //  格式化时间为yyyy-mm-dd格式
  formatDate: (date) => {
    let currentDate = new Date(date)
    let month = currentDate.getMonth() + 1 > 9 ? currentDate.getMonth() + 1 : '0' + (currentDate.getMonth() + 1)
    let day = currentDate.getDate() > 9 ? currentDate.getDate() : '0' + currentDate.getDate()
    return currentDate.getFullYear() + '-' + month + '-' + day
  },

  formatTime: (time) => {
    let currentTime = new Date(time)
    let hour = currentTime.getHours() < 10 ? '0' + currentTime.getHours() : currentTime.getHours()
    let minutes = currentTime.getMinutes() < 10 ? '0' + currentTime.getMinutes() : currentTime.getMinutes()
    let seconds = currentTime.getSeconds() < 10 ? '0' + currentTime.getSeconds() : currentTime.getSeconds()
    return currentTime.getFullYear() + '-' + (currentTime.getMonth() + 1) + '-' + currentTime.getDate() +
      ' ' + hour + ':' + minutes + ':' + seconds
  },

  //  格式化时间为yyyy-mm格式
  formatMonth: (date) => {
    let currentDate = new Date(date)
    let month = currentDate.getMonth() + 1 > 9 ? currentDate.getMonth() + 1 : '0' + (currentDate.getMonth() + 1)
    return currentDate.getFullYear() + '-' + month
  },
  //  获取上个月月份（不考虑日期）
  getLastMonth: () => {
    let currentDate = new Date()
    let thisYear = currentDate.getFullYear()
    let thisMonth = currentDate.getMonth()
    let year = ''
    let month = ''
    if (thisMonth === 0) {
      year = thisYear - 1
      month = 11
    } else {
      year = thisYear
      month = thisMonth - 1
    }
    month = month > 8 ? month + 1 : '0' + (month + 1)
    return year + '-' + month
  },

  //  获取今年的开始的日期
  getCurrentYearDate: () => {
    let currentDate = new Date()
    return currentDate.getFullYear() + '-01-01'
  },

  //  获取本月开始日期
  getCurrentMonthDate: () => {
    let currentDate = new Date()
    let month = null
    if (currentDate.getMonth() + 1 < 10) {
      month = '0' + (currentDate.getMonth() + 1)
    } else {
      month = currentDate.getMonth() + 1
    }
    return currentDate.getFullYear() + '-' + month + '-01'
  },

  //  获取日期格式根据传入的yyyy-MM-dd hh:mm:ss获取对应的时间
  formatDateByArg: (date, str) => {
    let formateDate = ''
    if (date) {
      formateDate = new Date(date)
    } else {
      formateDate = new Date()
    }
    let month = formateDate.getMonth() + 1 > 9 ? formateDate.getMonth() + 1 : '0' + (formateDate.getMonth() + 1)
    let day = formateDate.getDate() > 9 ? formateDate.getDate() : '0' + formateDate.getDate()
    let hour = formateDate.getHours() < 10 ? '0' + formateDate.getHours() : formateDate.getHours()
    let minutes = formateDate.getMinutes() < 10 ? '0' + formateDate.getMinutes() : formateDate.getMinutes()
    let seconds = formateDate.getSeconds() < 10 ? '0' + formateDate.getSeconds() : formateDate.getSeconds()
    str = str.replace('yyyy', formateDate.getFullYear())
    str = str.replace('MM', month)
    str = str.replace('dd', day)
    str = str.replace('hh', hour)
    str = str.replace('mm', minutes)
    str = str.replace('ss', seconds)
    return str
  }
}
