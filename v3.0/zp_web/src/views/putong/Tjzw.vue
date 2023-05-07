<template>
    <div class="app_data">
        <div class="title_data">
            <h2>推荐职位</h2>
        </div>
        <div class="update">
            <Table border :columns="columns1" :data="data1" max-height="670" stripe>
                <template #caozuo="{ row, index }">
                    <Rate v-model="row.is_collect" count="1" clearable @on-change="collect(row)"/>
                    <Button type="success" size="small" style="margin-right: 5px" @click="openInfo(row.job_href)">职位信息</Button>
                </template>
            </Table>
            <div class="page">
                <Page :total=pageInfo.total @on-change="ChangePage" show-total/>
            </div>
        </div>
    </div>
</template>
<script>
import {delData, t, getXueli} from "@/api";
import {zwtj} from "../../api";
import {collect,delCollect} from "@/api/index";

export default {
    data() {
        return {
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
                    width: '240'
                },
                {
                    title: '薪资',
                    align: 'center',
                    key: 'salary'
                },
                // {
                //     title: '行业类型',
                //     align:'center',
                //     key: 'hangye'
                // },
                {
                    title: '公司',
                    key: 'company',
                    align: 'center',
                    width: '240'
                },
                {
                    title: '工作地点',
                    key: 'location',
                    align: 'center',
                    width: 100
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
                    title: '爬取关键词',
                    align: 'center',
                    key: 'search'
                },
                {
                    title: '发布时间',
                    align: 'center',
                    key: 'pub_time',
                    width: 120
                },
                {
                    title: '操作',
                    slot: 'caozuo',
                    align: 'center',
                    width: 260
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
        handleSubmit() {
            this.init()
        },
        async init() {
            const {data:res} = await zwtj(this.pageInfo);
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
