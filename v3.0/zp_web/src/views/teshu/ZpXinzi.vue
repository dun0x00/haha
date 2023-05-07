<template>
    <div class="app_data">
        <div class="title">
            <h2>薪资统计</h2>
            <span>应用Python爬虫、Flask框架、Echarts、VUE等技术实现.</span>
        </div>
        <div class="query-c">
            <Form inline>
                <FormItem>
                    <Input type="text" v-model="searchParams.search" placeholder="职业类型"> </Input>
                </FormItem>
                <FormItem>
                    <Select v-model="searchParams.xueli" style="width:200px" placeholder="请选择学历"  clearable filterable>
                        <Option v-for="item in xueliList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                </FormItem>
                <FormItem prop="user">
                    <Select v-model="searchParams.exp" style="width:200px" placeholder="请选择经验" clearable filterable>
                        <Option v-for="item in expList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                </FormItem>
                <FormItem>
                    <Input type="text" v-model="searchParams.location" placeholder="工作地点"> </Input>
                </FormItem>
                <FormItem>
                    <Button type="primary" @click="handleSubmit()">搜索</Button>
                </FormItem>
            </Form>
        </div>
        <div class="update">
            <div id="main" style="width: 100%; height: 500px"></div>
        </div>

    </div>
</template>
<script>
import {getTsDatas,delTsData,tsXueli,tsjingyan,zpXinziTs} from "../../api/teshu";

export default {
    name: 'hello',
    data() {
        return {
            eData: [],
            searchParams: {
                search: '',
                xueli: '',
                location: '',
                exp:''
            },
            xueliList: [],
            expList:[],
        }
    },
    mounted() {
        this.init()
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
        handleSubmit() {
            this.init();
        },
        async init() {
            const {data:res} = await zpXinziTs(this.searchParams);
            this.eData = res.info
            this.drawChart();
        },
        drawChart() {
            // 基于准备好的dom，初始化echarts实例
            var myChart = this.$echarts.init(document.getElementById('main'));


            // 指定图表的配置项和数据
            var option = {
                color: [
                    '#006cff', '#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff',
                    '#006cff', '#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff',
                    '#006cff', '#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff',
                    '#006cff', '#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff',
                    '#006cff', '#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff',
                    '#006cff', '#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff'
                ],
                legend: {
                    top: 'bottom',
                    textStyle: {
                        fontSize: 10,
                        color: '#000',
                    }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b} : {c} ({d}%)'
                },
                series: [
                    {
                        name: '薪资占比',
                        type: 'pie',
                        radius: ['20%', '50%'],
                        center: ['50%', '50%'],
                        roseType: 'radius',
                        itemStyle: {
                            borderRadius: 8
                        },
                        data: this.eData,
                    }
                ]
            };


            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
            // 跟着缩放
            window.addEventListener('resize', function () {
                // 让我们的图表调用 resize这个方法
                myChart.resize();
            });
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
</style>
