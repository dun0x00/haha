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
                    <Select v-model="pageInfo.xueli" style="width:200px" placeholder="请选择学历">
                        <Option v-for="item in xueliList" :value="item.value" :key="item.value">{{ item.label }}</Option>
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
                    <Button type="success" size="small" style="margin-right: 5px" @click="openInfo(row.job_href)">职位信息</Button>
                    <Button v-if="userRole == '1'" type="error" size="small" @click="remove(row.id)" style="margin-right: 5px"
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
import {delData, getdatas, getXueli} from "@/api";
import {collect,delCollect} from "@/api/index";
import {dataUtils} from "@/utils/dataUtils";

export default {
    data() {
        return {
            pageInfo: {
                pageNo: 1,
                pageSize: 10,
                total: 0,
                search: '',
                location: '',
                xueli: '',
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
                    minwidth: '240'
                },
                {
                    title: '薪资',
                    align: 'center',
                    key: 'salary',
                    width: '150'
                },
                {
                    title: '公司',
                    key: 'company',
                    align: 'center',
                    minwidth: '240'
                },
                {
                    title: '工作地点',
                    key: 'location',
                    align: 'center',
                    minwidth: 120
                },
                {
                    title: '经验',
                    key: 'jingyan',
                    align: 'center',
                    width: 120
                },
                {
                    title: '学历',
                    key: 'xueli',
                    align: 'center',
                    width: 100
                },
                {
                    title: '发布时间',
                    align: 'center',
                    key: 'pub_time',
                    width: 120
                },
                {
                    title: '爬取时间',
                    align: 'center',
                    key: 'create_time',
                    width: 120,
                    render: (h, params) => {
                        return h('div', {
                            props: {},
                            style: {}
                        }, dataUtils.formatDate(params.row.create_time))
                    }
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
            modal: false,
            id: '',
            userRole:localStorage.getItem('role'),
        }
    },
    mounted() {
        this.init()
        this.getXueliList()
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
        remove(e) {
            this.id = e
            this.modal = true
        },
        async asyncOK() {
            this.modal = false;
            const res = await delData(`id=${this.id}`);
            if (res.code == 200) {
                this.$Message.success(res.info);
                this.init()
            } else {
                this.$Message.error(res.info);
            }
        },
        handleSubmit() {
            this.init()
        },
        async getXueliList() {
            const {data:res} = await getXueli();
            // console.log(res);
            this.xueliList = res.info;
        },
        async init() {
            const {data:res} = await getdatas(this.pageInfo);
            this.pageInfo.total = res.total
            this.pageInfo.pageNo = res.pageno
            this.pageInfo.pageSize = res.pagesize
            // console.log(res.info);
            res.info.forEach( item => {
                item.pub_time = item.pub_time.substr(0, 11)
            })
            this.data1 = res.info
        },
        ChangePage(e) {
            this.pageInfo.pageNo = e
            this.init()
        },
        openInfo(e) {
            window.open(e)
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
