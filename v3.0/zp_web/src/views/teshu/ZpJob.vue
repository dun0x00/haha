<template>
    <div class="app_data">
        <div class="title">
            <h2>职位招聘分析</h2>
            <span>应用Python爬虫、Flask框架、Echarts、VUE等技术实现.</span>
        </div>
        <div class="query-c">
            <Form inline>
                <FormItem prop="user">
                    <Input type="text" v-model="searchParams.location" placeholder="工作地点"> </Input>
                </FormItem>
                <FormItem prop="user">
                    <Select v-model="searchParams.edu" style="width:200px" placeholder="请选择学历" clearable filterable>
                        <Option v-for="item in xueliList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                </FormItem>
                <FormItem prop="user">
                    <Select v-model="searchParams.exp" style="width:200px" placeholder="请选择经验" clearable filterable>
                        <Option v-for="item in expList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                </FormItem>
                <FormItem>
                    <Button type="primary" @click="handleSubmit()">搜索</Button>
                </FormItem>
            </Form>
        </div>
        <div class="update">
            <div id="main" style="width: 100%; height: 400px"></div>
        </div>

    </div>
</template>
<script>
import {tsJobTop,tsXueli,tsjingyan} from "../../api/teshu";

export default {
    name: 'hello',
    data() {
        return {
            eData: [],
            xData:[],
            yData:[],
            searchParams:{
                location:'',
                edu:'',
                exp:''
            },
            xueliList: [],
            expList:[],
            typeList:[
                {label:'省级',value:'1'},
                {label:'市级',value:'2'},
                {label:'县（区）级',value:'3'}
            ]
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

        // 搜索
        handleSubmit() {
            this.xData = []
            this.yData = []
            this.init();
        },

        // 数据查询
        async init() {
            const {data:res} = await tsJobTop(this.searchParams);
            res.info.forEach(item =>{
                this.xData.push(item.name)
                this.yData.push(item.value)
            })
            this.drawChart();
        },

        // echarts 绘制
        drawChart() {
            // 基于准备好的dom，初始化echarts实例
            var myChart = this.$echarts.init(document.getElementById('main'));

            var myColor = [
                "#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6",
                "#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6",
                "#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6",
                "#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6",
                "#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6",
                "#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6",
                "#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6",
            ];

            // 指定图表的配置项和数据
            var option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                grid: {
                    top: "10%",
                    left: '3%',
                    right: '6%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: this.xData,
                    //主要是下面的代码-倾斜
                    axisLabel:{
                        rotate : 60
                    }
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '招聘公司数',
                        type: 'bar',
                        // 柱子设为圆角
                        itemStyle: {
                            normal: {
                                barBorderRadius: 20,
                                // dataIndex 是当前柱子的索引号
                                color: function (params) {
                                    return myColor[params.dataIndex];
                                }
                            }
                        },
                        data: this.yData,
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
