import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const commonRoutes = [
    {
        path: '/login',
        name: 'login',
        meta: { title: '登录' },
        component: () => import('../components/Login.vue'),
    },
    {
        path: '/reg',
        name: 'reg',
        meta: { title: '注册' },
        component: () => import('../components/Reg.vue'),
    },
    {
        path: '/404',
        name: '404',
        meta: { title: '404' },
        component: () => import('../components/404.vue'),
    },
    { path: '/', redirect: '/userInfo' },
]

// 本地所有的页面 需要配合后台返回的数据生成页面
export const asyncRoutes = {
    /** ************************** 管理员页面 通用页面 ****************************/
    userInfo: {
        path: 'userInfo',
        name: 'userInfo',
        meta: { title: '个人信息' },
        component: () => import('../views/UserInfo.vue'),
    },
    password: {
        path: 'password',
        name: 'password',
        meta: { title: '修改密码' },
        component: () => import('../views/Password.vue'),
    },
    getdata: {
        path: 'getdata',
        name: 'getdata',
        meta: { title: '获取数据' },
        component: () => import('../views/admin/GetData.vue'),
    },
    datalog: {
        path: 'datalog',
        name: 'datalog',
        meta: { title: '爬取日志' },
        component: () => import('../views/admin/Datalog.vue'),
    },
    userlist: {
        path: 'userlist',
        name: 'userlist',
        meta: { title: '用户管理' },
        component: () => import('../views/admin/Userlist.vue'),
    },
    /** ************************** 普通用户页面 ****************************/
    data: {
        path: 'data',
        name: 'data',
        meta: { title: '数据概览' },
        component: () => import('../views/putong/Data.vue'),
    },
    zpcity: {
        path: 'zpcity',
        name: 'zpcity',
        meta: { title: '城市招聘分布' },
        component: () => import('../views/putong/Zpcity.vue'),
    },
    jobTop: {
        path: 'jobTop',
        name: 'jobTop',
        meta: { title: '职位招聘分析' },
        component: () => import('../views/putong/ZpJob.vue'),
    },
    zpfuli: {
        path: 'zpfuli',
        name: 'zpfuli',
        meta: { title: '福利词云' },
        component: () => import('../views/putong/ZpFuli.vue'),
    },
    zpxinzi: {
        path: 'zpxinzi',
        name: 'zpxinzi',
        meta: { title: '薪资统计' },
        component: () => import('../views/putong/ZpXinzi.vue'),
    },
    zpyaoqiu: {
        path: 'zpyaoqiu',
        name: 'zpyaoqiu',
        meta: { title: '招聘要求' },
        component: () => import('../views/putong/ZpYaoqiu.vue'),
    },
    gsinfo: {
        path: 'gsinfo',
        name: 'gsinfo',
        meta: { title: '公司信息分析' },
        component: () => import('../views/putong/ZpGs.vue'),
    },
    tjzw: {
        path: 'tjzw',
        name: 'tjzw',
        meta: { title: '推荐职位' },
        component: () => import('../views/putong/Tjzw.vue'),
    },
    yuce: {
        path: 'yuce',
        name: 'yuce',
        meta: { title: '薪资预测' },
        component: () => import('../views/putong/Xzyc.vue'),
    },
    /** ************************** 特殊用户页面 ****************************/
    dataTeshu: {
        path: 'dataTeshu',
        name: 'dataTeshu',
        meta: { title: '数据概览' },
        component: () => import('../views/teshu/Data.vue'),
    },
    zpcityTs: {
        path: 'zpcityTs',
        name: 'zpcityTs',
        meta: { title: '城市招聘需求分布' },
        component: () => import('../views/teshu/Zpcity.vue'),
    },
    tsJobTop: {
        path: 'tsJobTop',
        name: 'tsJobTop',
        meta: { title: '职位招聘分析' },
        component: () => import('../views/teshu/ZpJob.vue'),
    },
    zpfuliTs: {
        path: 'zpfuliTs',
        name: 'zpfuliTs',
        meta: { title: '标签词云' },
        component: () => import('../views/teshu/Cloud.vue'),
    },
    zpxinziTs: {
        path: 'zpxinziTs',
        name: 'zpxinziTs',
        meta: { title: '薪资统计' },
        component: () => import('../views/teshu/ZpXinzi'),
    },
    zpyaoqiuTs: {
        path: 'zpyaoqiuTs',
        name: 'zpyaoqiuTs',
        meta: { title: '招聘要求' },
        component: () => import('../views/teshu/ZpYaoqiu.vue'),
    },
    gsinfoTs: {
        path: 'gsinfoTs',
        name: 'gsinfoTs',
        meta: { title: '公司信息分析' },
        component: () => import('../views/teshu/ZpGs.vue'),
    },
    tjzwTs: {
        path: 'tjzwTs',
        name: 'tjzwTs',
        meta: { title: '推荐职位' },
        component: () => import('../views/teshu/Tjzw.vue'),
    },
    yuceTs: {
        path: 'yuceTs',
        name: 'yuceTs',
        meta: { title: '薪资预测' },
        component: () => import('../views/teshu/Xzyc.vue'),
    },
}

const createRouter = () => new Router({
    routes: commonRoutes,
})

const router = createRouter()

export function resetRouter() {
    const newRouter = createRouter()
    router.matcher = newRouter.matcher
}

export default router
