import request from '@/utils/request'

// 特殊用户相关api

// 数据概览
export function getTsDatas(params) {
    return request.post('/api/getTsDatas' , params)
}

// 删除
export function delTsData(params) {
    return request.post('/api/delTsData' , params)
}

// 学历
export function tsXueli(params) {
    return request.post('/api/tsXueli' , params)
}

// 经验
export function tsjingyan(params) {
    return request.post('/api/tsjingyan' , params)
}

// 城市招聘分布
export function tszpcity(params) {
    return request.post('/api/tszpcity' , params)
}

// 职位招聘分析
export function tsJobTop(params) {
    return request.post('/api/tsJobTop' , params)
}

// 生成标签词云
export function cloudTs(params) {
    return request.post('/api/cloudTs' , params)
}

// 薪资统计
export function zpXinziTs(params) {
    return request.post('/api/zpXinziTs' , params)
}

// 招聘要求
export function yaoqiuTs(params) {
    return request.post('/api/yaoqiuTs' , params)
}

// 公司信息分析
export function gsinfoTs(params) {
    return request.post('/api/gsinfoTs' , params)
}

// 职位推荐
export function zwtjTs(params) {
    return request.post('/api/zwtjTs' , params)
}

// 薪资预测
export function yuceTs(params) {
    return request.post('/api/yuceTs' , params)
}

// 查询所有城市
export function citysTs(params) {
    return request.post('/api/citysTs' , params)
}
