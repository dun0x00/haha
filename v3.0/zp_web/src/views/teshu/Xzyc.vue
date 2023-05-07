<template>
    <div class="app_data">
        <div class="title">
            <h2>薪资预测</h2>
            <span>应用Python爬虫、Flask框架、Echarts、VUE等技术实现.</span>
        </div>
        <div class="update">
                <Form ref="formInline" :model="formLeft" :rules="formLeft" inline style="text-align: center;padding-top: 20px;">
                    <div>
                        <FormItem prop="search">
                            <Input v-model="formLeft.search" placeholder="行业"></Input>
                        </FormItem>
                        <FormItem prop="location">
                            <Input v-model="formLeft.location" placeholder="工作地点"></Input>
                        </FormItem>
                        <FormItem prop="xueli">
                            <FormItem>
                                <Select v-model="formLeft.xueli" style="width:200px" placeholder="请选择学历" clearable>
                                    <Option v-for="item in xueliList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </Select>
                            </FormItem>
                        </FormItem>
                    </div>

                    <div>
                        <FormItem prop="user">
                            <Select v-model="formLeft.jingyan" style="width:200px" placeholder="请选择工作经验" clearable>
                                <Option v-for="item in jingyanList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                            </Select>
                        </FormItem>
                        <FormItem prop="user">
                            <Select v-model="formLeft.company" style="width:200px" placeholder="请选择公司规模" clearable>
                                <Option v-for="item in companySize" :value="item.value" :key="item.value">{{ item.label }}</Option>
                            </Select>
                        </FormItem>
                        <FormItem prop="user">
                            <Select v-model="formLeft.companytype_text" style="width:200px" placeholder="请选择公司性质" clearable>
                                <Option v-for="item in companyXz" :value="item.value" :key="item.value">{{ item.label }}</Option>
                            </Select>
                        </FormItem>
                    </div>
                    <div>
                        <FormItem>
                            <Button type="success" @click="handleSubmit('formInline')">开始预测</Button>
                        </FormItem>
                    </div>

                </Form>
                <div class="xinzi">
                    <div class="xinzi_d">
                        <p class="xinzi_x" v-if="xinzi > 0" >最低薪资：￥{{ xinzimin }}</p>
                        <p class="xinzi_x" v-if="xinzi > 0" >最高薪资：￥{{ xinziMax }}</p>
                        <p class="xinzi_x" v-if="xinzi > 0" >薪资平均数：￥{{ xinziAvg }}</p>
                        <p class="xinzi_x" v-if="xinzi > 0" >薪资中位数：￥{{ xinzi }}</p>
                        <p v-if="xinzi > 0" >（结果仅供参考）</p>
                        <span v-if="xinzi == 0" >暂无结果，请爬取更多数据或更换查询条件重试</span>
                    </div>
                </div>
        </div>

    </div>
</template>
<script>
import {tszpcity,tsXueli,tsjingyan,yuceTs} from "../../api/teshu";
export default {
    data() {
        return {
            formLeft: {
                search:'',
                location: '',
                xueli: '',
                jingyan:'',
                company:'',
                companytype_text:''
            },
            log:'',
            xinzi:-1,
            xinziAvg:0,
            xinziMax:0,
            xinzimin:0,
            xueliList: [],
            jingyanList:[],
            companySize:[
                {value:'30人以下',label:'30人以下'},
                {value:'30-99人',label:'30-99人'},
                {value:'100-499人',label:'100-499人'},
                {value:'500-999人',label:'500-999人'},
                {value:'1000-9999人',label:'1000-9999人'},
                {value:'10000人以上',label:'10000人以上'},
            ],
            companyXz:[
                {value:'外商独资',label:'外商独资'},
                {value:'民营',label:'民营'},
                {value:'股份制企业',label:'股份制企业'},
                {value:'国企',label:'国企'},
                {value:'上市公司',label:'上市公司'},
                {value:'合资',label:'合资'},
                {value:'事业单位',label:'事业单位'},
                {value:'代表处',label:'代表处'},
                {value:'其它',label:'其它'},
            ]
        }
    },
    mounted() {
        this.getXueliList()
        this.getJIngyan()
    },
    methods:{
        async getJIngyan() {
            const {data:res} = await tsjingyan();
            this.jingyanList = res.info;
        },
        async getXueliList() {
            const  {data:res} = await tsXueli();
            this.xueliList = res.info;
        },
        async handleSubmit() {
            const  {data:res} = await yuceTs(this.formLeft)
            this.xinzi = res.info
            this.xinziAvg = res.info2[0].avg
            this.xinziMax = res.info2[0].max
            this.xinzimin = res.info2[0].min
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

.title h2{
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 20px;
    padding-bottom: 0;
    color: #5c768d;
}

.title span{
    font-size: 16px;
    color: #444;
    font-family: "Open Sans", sans-serif;
}

.update {
    background: #f5f9fc;
}
.xinzi{
    padding: 10px 50px 50px 50px;
    text-align: center;
    height: 375px;
}
.xinzi_d{
    background: #e8e9f3;
    height: 100%;
    padding: 3% 0 0 0;
    width: 50%;
    margin-left: 25%;
    text-align: center;
}
.xinzi_x{
    font-family: emoji;
    font-size: 32px;
    color: #f55512;
    font-weight: 600;
}
</style>
