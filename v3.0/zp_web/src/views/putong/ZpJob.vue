<template>
    <div class="app_data">
        <div class="title">
            <h2>职位招聘分析</h2>
            <span>应用Python爬虫、Flask框架、Echarts、VUE等技术实现.</span>
        </div>
        <div class="query-c">
            <Form inline>
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
import {jobTop} from "@/api";

export default {
    name: 'hello',
    data() {
        return {
            eData: [],
            xData:[],
            yData:[],
            searchParams:{
                location:''
            }
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        handleSubmit() {
            this.xData = []
            this.yData = []
            this.init();
        },

        async init() {
            const {data:res} = await jobTop(this.searchParams);
            res.info.forEach(item =>{
                this.xData.push(item.name)
                this.yData.push(item.value)
            })
            this.drawChart();
        },

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
