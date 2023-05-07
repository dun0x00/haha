<template>
    <div class="app_data">
        <div class="title">
            <h2>招聘标签词云图</h2>
            <span>应用Python爬虫、Flask框架、Echarts、VUE等技术实现.</span>
        </div>
        <div class="query-c">
            <Form inline>
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
                    <Button type="primary" @click="handleSubmit()">更新词云</Button>
                </FormItem>
            </Form>
        </div>
        <div class="update">
            <div class="img-show">
                <img src="../../assets/imgs/cloud/fuliColoud.png">
            </div>
        </div>

    </div>
</template>
<script>
import {cloudTs,tsXueli,tsjingyan} from "@/api/teshu";

export default {
    name: 'hello',
    data() {
        return {
            pageInfo: {
                search: '',
                location: '',
                xueli: '',
                exp:'',
            },
            xueliList:[],
            expList:[]
        }
    },
    mounted() {
        this.getXueliList()
        this.getExpList()
    },
    methods: {
        // 学历列表
        async getXueliList() {
            const {data:res} = await tsXueli();
            this.xueliList = res.info;
        },
        // 经验列表
        async getExpList(){
            const {data:res} = await tsjingyan();
            this.expList = res.info;
        },
        async handleSubmit() {
            const {data:res} = await cloudTs(this.pageInfo)
            if (res.code == 200) {
                this.$Message.success(res.info);
            } else {
                this.$Message.error(res.info);
            }
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

.title {
    margin: 4px auto;
    padding: 30px;
    text-align: center;
}

.title h2 {
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 20px;
    padding-bottom: 0;
    color: #5c768d;
}

.title span {
    font-size: 16px;
    color: #444;
    font-family: "Open Sans", sans-serif;
}

.update {
    background: #f5f9fc;
}

.img-show {
    text-align: center;
    padding: 20px;
}
</style>
