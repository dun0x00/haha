<template>
    <div class="app_data">
        <div class="title_data">
            <h2>推荐职位</h2>
        </div>

        <div class="update">
            <Table border :columns="columns1" :data="data1" max-height="670" stripe>
                <template #caozuo="{ row, index }">
                    <Rate v-model="row.is_collect" count="1" clearable @on-change="collect(row)"/>
                    <Button type="primary" size="small" style="margin-right: 5px" @click="openDetail(row.job_id,row.companyInfo_id)">公司信息</Button>
                    <Button type="success" size="small" style="margin-right: 5px" @click="openInfo(row.job_id,row.companyInfo_id)">职位信息</Button>
                </template>
            </Table>
            <div class="page">
                <Page :total=pageInfo.total @on-change="ChangePage" show-total/>
            </div>
        </div>
    </div>
</template>
<script>
import {zwtjTs,delTsData,tsXueli,tsjingyan} from "../../api/teshu";
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
                account: localStorage.getItem('account'),
                user_id: localStorage.getItem('userId'),
            },
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
                    width: 260
                },

            ],
            data1: [],
            modal: false,
            id: '',
            userRole: localStorage.getItem('role'),
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        // 收藏
        collect(e) {
            let params = {
                user_id:localStorage.getItem('userId'),
                job_id:e.id
            }
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
            const {data:res} = await delTsData(`id=${this.id}`);
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
        // 列表数据
        async init() {
            const {data:res} = await zwtjTs(this.pageInfo);
            if (res.code == 200) {
                if (!res.info.length) {
                    this.$Message.warning("暂无合适的职位")
                }
                this.pageInfo.total = res.total
                this.pageInfo.pageNo = res.pageno
                this.pageInfo.pageSize = res.pagesize
                this.data1 = res.info
            } else {
                this.$Message.warning(res.info)
            }
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
