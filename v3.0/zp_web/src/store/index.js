import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        // isShowLoading: false, // 全局 loading
        // 左侧菜单栏数据
        menuItems: [
            /** ************************** 管理员菜单 ****************************/
            {
                text: '个人中心',
                type: 'ios-paper',
                role: '1',
                children: [
                    {
                        type: 'md-lock',
                        name: 'userInfo',
                        text: '个人信息',
                    },
                    {
                        type: 'md-lock',
                        name: 'password',
                        text: '修改密码',
                    },
                ],
            },
            {
                text: '数据管理',
                type: 'ios-paper',
                role: '1',
                children: [
                    {
                        type: 'ios-browsers-outline',
                        name: 'data',
                        text: '智联数据概览',
                    },
                    {
                        type: 'ios-browsers-outline',
                        name: 'dataTeshu',
                        text: '残疾人招聘数据概览',
                    },
                    {
                        type: 'md-person',
                        name: 'getdata',
                        text: '智联数据获取',
                    },
                    {
                        type: 'md-person',
                        name: 'datalog',
                        text: '数据爬取日志',
                    },

                ],
            },
            {
                type: 'md-person',
                name: 'userlist',
                text: '用户管理',
                role: '1',
            },

            /** ************************** 普通用户菜单 ****************************/
            {
                text: '个人中心',
                type: 'ios-paper',
                role: '2',
                children: [
                    {
                        type: 'md-lock',
                        name: 'userInfo',
                        text: '个人信息',
                    },
                    {
                        type: 'md-lock',
                        name: 'password',
                        text: '修改密码',
                    },
                ],
            },
            {
                text: '职位概览',
                type: 'ios-paper',
                role: '2',
                children: [
                    {
                        type: 'ios-paper',
                        name: 'data',
                        text: '职位数据',
                    },
                    {
                        type: 'md-person',
                        name: 'getdata',
                        text: '数据获取',
                    },
                    {
                        type: 'md-person',
                        name: 'datalog',
                        text: '数据爬取日志',
                    },
                ]
            },
            {
                text: '数据可视化',
                type: 'ios-paper',
                role: '2',
                children: [
                    {
                        type: 'ios-list-box-outline',
                        name: 'zpcity',
                        text: '城市招聘分布',
                    },
                    {
                        type: 'ios-list-box-outline',
                        name: 'jobTop',
                        text: '职位招聘分析',
                    },
                    {
                        type: 'ios-cloud-outline',
                        name: 'zpfuli',
                        text: '福利词云',
                    },
                    {
                        type: 'ios-stats-outline',
                        name: 'zpxinzi',
                        text: '薪资统计',
                    },
                    {
                        type: 'ios-paper-outline',
                        name: 'zpyaoqiu',
                        text: '招聘要求',
                    },
                    {
                        type: 'ios-information-circle-outline',
                        name: 'gsinfo',
                        text: '公司信息分析',
                    },

                ],
            },
            {
                type: 'ios-paper-plane-outline',
                name: 'tjzw',
                text: '推荐职位',
                role: '2',
            },
            {
                type: 'ios-paper-plane-outline',
                name: 'yuce',
                text: '薪资预测',
                role: '2',
            },

            /** ************************** 特殊用户菜单 ****************************/
            {
                text: '个人中心',
                type: 'ios-paper',
                role: '3',
                children: [
                    {
                        type: 'md-lock',
                        name: 'userInfo',
                        text: '个人信息',
                    },
                    {
                        type: 'md-lock',
                        name: 'password',
                        text: '修改密码',
                    },
                ],
            },
            {
                text: '职位数据',
                type: 'ios-paper',
                role: '3',
                name: 'dataTeshu',
            },
            {
                text: '数据可视化',
                type: 'ios-paper',
                role: '3',
                children: [
                    {
                        type: 'ios-list-box-outline',
                        name: 'zpcityTs',
                        text: '城市招聘分布',
                    },
                    {
                        type: 'ios-list-box-outline',
                        name: 'tsJobTop',
                        text: '职位招聘分析',
                    },
                    {
                        type: 'ios-cloud-outline',
                        name: 'zpfuliTs',
                        text: '标签词云',
                    },
                    {
                        type: 'ios-stats-outline',
                        name: 'zpxinziTs',
                        text: '薪资统计',
                    },
                    {
                        type: 'ios-paper-outline',
                        name: 'zpyaoqiuTs',
                        text: '招聘要求',
                    },
                    {
                        type: 'ios-information-circle-outline',
                        name: 'gsinfoTs',
                        text: '公司信息分析',
                    },

                ],
            },
            {
                type: 'ios-paper-plane-outline',
                name: 'tjzwTs',
                text: '推荐职位',
                role: '3',
            },
            {
                type: 'ios-paper-plane-outline',
                name: 'yuceTs',
                text: '薪资预测',
                role: '3',
            },


        ],
    },
    mutations: {
        setMenus(state, items) {
            state.menuItems = [...items]
        },
        setLoading(state, isShowLoading) {
            state.isShowLoading = isShowLoading
        },
    },
})

export default store
