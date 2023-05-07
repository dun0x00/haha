<template>
    <div class="app_data">
        <div class="title_data">
            <h2>数据概览</h2>
        </div>
        <div class="query-c">
            <Form inline>
                <FormItem prop="user">
                    <Select v-model="pageInfo.searchType" style="width:200px">
                        <Option v-for="item in searchTypeList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                </FormItem>
                <FormItem prop="user">
                    <Input type="text" v-model="pageInfo.search" placeholder="职位名称"> </Input>
                </FormItem>
                <FormItem prop="user">
                    <Input type="text" v-model="pageInfo.location" placeholder="工作地点"> </Input>
                </FormItem>
                <FormItem prop="user">
                    <Select v-model="pageInfo.xueli" style="width:200px" placeholder="请选择学历" clearable filterable>
                        <Option v-for="item in xueliList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                </FormItem>
                <FormItem prop="user">
                    <Select v-model="pageInfo.exp" style="width:200px" placeholder="请选择经验" clearable filterable>
                        <Option v-for="item in expList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                </FormItem>
                <FormItem>
                    <Button type="primary" @click="handleSubmit('formInline')">搜索</Button>
                </FormItem>
            </Form>
        </div>
        <div class="update">
            <Table border :columns="columns1" :data="data1" max-height="670" stripe>
                <template #caozuo="{ row, index }">
                    <Rate v-model="row.is_collect" :count="1" clearable @on-change="collect(row)"/>
                    <Button type="primary" size="small" style="margin-right: 5px" @click="openDetail(row.job_id,row.companyInfo_id)">公司信息</Button>
                    <Button type="success" size="small" style="margin-right: 5px" @click="openInfo(row.job_id,row.companyInfo_id)">职位信息</Button>
                    <Button v-if="userRole == '1'" type="error" size="small" @click="remove(row.job_id)" style="margin-right: 5px"
                    >删除
                    </Button
                    >
                </template>
            </Table>
            <div class="page">
                <Page :total=pageInfo.total @on-change="ChangePage" show-total/>
            </div>
        </div>
        <!-- 删除提示框 -->
        <Modal
            v-model="modal"
            title="提示"
            @on-ok="asyncOK">
            <p>确定要删除吗</p>
        </Modal>
    </div>
</template>
<script>
import {getTsDatas,delTsData,tsXueli,tsjingyan} from "../../api/teshu";
import {collect,delCollect} from "@/api/index";
import {dataUtils} from "@/utils/dataUtils";

export default {
    data() {
        return {
            formatDate: dataUtils.formatDate,
            pageInfo: {
                pageNo: 1,
                pageSize: 10,
                total: 0,
                search: '',
                location: '',
                xueli: '',
                exp:'',
                user_id: localStorage.getItem('userId'),
                searchType:'1'
            },
            searchTypeList: [
                {label:'查看全部',value:'1'},
                {label:'查看我的收藏',value:'0'},
            ],
            columns1: [
                {
                    title: '标题',
                    key: 'job_name',
                    align: 'center',
                },
                {
                    title: '薪资',
                    align: 'center',
                    key: 'job_salary',
                    width: '100'
                },
                {
                    title: '公司',
                    key: 'company_name',
                    align: 'center',
                    width: '240'
                },
                {
                    title: '工作地点',
                    key: 'provinceid',
                    align: 'center',
                    width: 180,
                    render: (h, params) => {
                        return h('div', {
                            props: {},
                            style: {}
                        }, params.row.provinceid + '-' + params.row.cityid + '-' + params.row.three_cityid)
                    }
                },
                {
                    title: '经验',
                    key: 'exp',
                    align: 'center',
                    width: 100
                },
                {
                    title: '学历',
                    key: 'edu',
                    align: 'center',
                    width: 100
                },
                {
                    title: '招聘时间',
                    align: 'center',
                    key: 'update_time',
                    width:'200',
                    render: (h, params) => {
                        return h('div', {
                            props: {},
                            style: {}
                        }, dataUtils.formatDate(params.row.begin_time) + '-' + dataUtils.formatDate(params.row.end_time) )
                    }
                },
                {
                    title: '发布时间',
                    align: 'center',
                    key: 'update_time',
                    width: 150
                },
                {
                    title: '操作',
                    slot: 'caozuo',
                    align: 'center',
                    minwidth: 260
                },

            ],
            data1: [],
            xueliList: [],
            expList:[],
            modal: false,
            id: '',
            userRole: localStorage.getItem('role'),
        }
    },
    mounted() {
        this.init()
        this.getXueliList()
        this.getExpList()
    },
    methods: {
        // 收藏
        collect(e) {
            let params = {
                user_id:localStorage.getItem('userId'),
                job_id:e.job_id
            }
            // console.log(params);
            if (e.is_collect === 0) {
                // 已收藏，取消收藏
                delCollect(params).then(res => {
                    const result = res.data
                    if (result && result.code === '200') {
                        this.$Message.success("取消收藏成功")
                    } else {
                        this.$Message.error("取消收藏失败")
                    }
                    this.init()
                })
            } else {
                // 未收藏，开始收藏
                collect(params).then(res => {
                    const result = res.data
                    // console.log(res);
                    if (result && result.code === '200') {
                        this.$Message.success("收藏成功")
                    } else {
                        this.$Message.error("收藏失败")
                    }
                    this.init()
                })
            }
        },
        // 删除
        remove(e) {
            this.id = e
            this.modal = true
        },
        async asyncOK() {
            this.modal = false;
            const res = await delTsData(`id=${this.id}`);
            if (res.code == 200) {
                this.$Message.success(res.info);
                this.init()
            } else {
                this.$Message.error(res.info);
            }
        },
        // 查询
        handleSubmit() {
            this.pageInfo.pageNo = 1
            this.init()
        },
        // 学历列表
        async getXueliList() {
            const {data:res} = await tsXueli();
            // console.log(res);
            this.xueliList = res.info;
        },
        // 经验列表
        async getExpList(){
            const {data:res} = await tsjingyan();
            this.expList = res.info;
        },
        // 列表数据
        async init() {
            const {data:res} = await getTsDatas(this.pageInfo);
            this.pageInfo.total = res.total
            this.pageInfo.pageNo = res.pageno
            this.pageInfo.pageSize = res.pagesize
            this.data1 = res.info
        },
        // 翻页
        ChangePage(e) {
            this.pageInfo.pageNo = e
            this.init()
        },
        // 打开详情
        openDetail(job_id,companyInfo_id) {
            const href = 'https://www.cdpee.org.cn/job/businessDetails/?id='+job_id+'&companyId=' + companyInfo_id
            window.open(href)
        },
        // 打开公司信息
        openInfo(job_id,companyInfo_id) {
            const href = 'https://www.cdpee.org.cn/job/jobDetail/?id='+job_id+'&companyId=' + companyInfo_id
            window.open(href)
        }
    }
}
</script>
<style>
.app_data {
    width: 100%;
    height: 100%;
    background: #ffffff;
    padding: 0 10px;
    font-family: "Open Sans", sans-serif;
    color: #444;
}

.title_data {
    margin: 4px auto;
    padding: 15px;
    text-align: center;
}

.title_data h2 {
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 20px;
    padding-bottom: 0;
    color: #5c768d;
}

.title_data span {
    font-size: 16px;
    color: #444;
    font-family: "Open Sans", sans-serif;
}

.update {
    background: #f5f9fc;
}

.page {
    text-align: center;
    padding: 10px;
}

.query-c {
    margin: 0 0 -12px 0;
}
</style>
