<template>
    <div class="app_pwd" style="margin-top: 5px;height: 100%" >
        <div class="form">
            <Form ref="formCustom" :model="formCustom" :rules="ruleCustom" :label-width="80">
                <FormItem label="账号:" prop="account">
                    <span class="fn-style">{{ account }}</span>
                </FormItem>
                <FormItem label="角色:" prop="account">
                    <span class="fn-style" v-if="formCustom.role === '1'">系统管理员</span>
                    <span class="fn-style" v-if="formCustom.role === '2'">普通用户</span>
                    <span class="fn-style" v-if="formCustom.role === '3'">特殊用户</span>
                </FormItem>
                <FormItem label="姓名:" prop="name">
                    <Input type="text" v-model="formCustom.name"></Input>
                </FormItem>
                <FormItem label="邮箱:" prop="email">
                    <Input type="text" v-model="formCustom.email"></Input>
                </FormItem>
                <FormItem label="电话:" prop="phone">
                    <Input type="text" v-model="formCustom.phone"></Input>
                </FormItem>
                <FormItem label="头像:" prop="icon">
                    <Input type="text" v-model="formCustom.img"></Input>
                </FormItem>
                <FormItem label="备注:" prop="remarks">
                    <Input type="text" v-model="formCustom.remarks"></Input>
                </FormItem>
                <FormItem label="工作地点:" prop="remarks">
                    <Input type="text" v-model="formCustom.location"></Input>
<!--                    <Select v-model="formCustom.location" style="width:200px" placeholder="请选择工作地点" clearable filterable>
                        <Option v-for="item in cityList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>-->
                </FormItem>
                <FormItem label="经验:" prop="remarks">
                    <Select v-model="formCustom.exp" style="width:200px" placeholder="请选择经验" clearable filterable>
                        <Option v-for="item in expList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                </FormItem>
                <FormItem label="学历:" prop="remarks">
                    <Select v-model="formCustom.deu" style="width:200px" placeholder="请选择学历" clearable filterable>
                        <Option v-for="item in xueliList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                </FormItem>
                <FormItem label="专业:" prop="remarks">
                    <Input type="text" v-model="formCustom.major"></Input>
                </FormItem>
                <FormItem style="text-align: center">
                    <Button type="primary" @click="handleSubmit('formCustom')">提交</Button>
                    <Button @click="handleReset('formCustom')" style="margin-left: 8px">重置</Button>
                </FormItem>
            </Form>
        </div>
    </div>
</template>
<script>
import { editUser, userInfo,getXueli} from "@/api";
import {resetTokenAndClearUser} from "../utils";
import {tsXueli,citysTs} from "../api/teshu";

export default {
    data() {
        const name = (rule, value, callback) => {
            if (!value) {
                callback(new Error('请输入姓名'));
            } else {
                callback();
            }
        };
        const email = (rule, value, callback) => {
            if (!value) {
                callback(new Error('请输入邮箱'));
            } else {
                callback();
            }
        };
        const phone = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('请输入电话'));
            } else {
                callback();
            }
        };
        return {
            xueliList: [],
            cityList:[],
            expList:[],
            account: localStorage.getItem('account') || '',
            formCustom: {},
            ruleCustom: {
                name: [
                    {validator: name, trigger: 'blur'}
                ],
                email: [
                    {validator: email, trigger: 'blur'}
                ],
                phone: [
                    {validator: phone, trigger: 'blur'}
                ]
            }
        }
    },
    mounted() {
        this.userInfo()
    },
    methods: {
        // 城市列表
        async getCiyts() {
            const {data:res} = await citysTs();
            this.cityList = res.info;
        },
        // 学历列表
        async getXuelist() {
            const {data:res} = await tsXueli();
            this.xueliList = res.info;
        },
        async getXueliPt() {
            const {data:res} = await getXueli();
            this.xueliList = res.info;
        },
        // 用户信息
        async userInfo() {
            const {data:res} = await userInfo(`account=${this.account}`)
            // console.log(res);
            if (res.code == 200) {
                this.formCustom = res.info[0]
                if(this.formCustom.role && this.formCustom.role == '3') {
                    // this.getXueliList()
                    this.getXuelist()
                    this.expList = [
                        {label:'应届毕业生',value:'99'},
                        {label:'无经验',value:'0'},
                        {label:'一年',value:'1'},
                        {label:'二年',value:'2'},
                        {label:'三年',value:'3'},
                        {label:'四年',value:'4'},
                        {label:'五年',value:'5'},
                        {label:'六年',value:'6'},
                        {label:'七年',value:'7'},
                        {label:'八年',value:'8'},
                        {label:'九年',value:'9'},
                        {label:'十年',value:'10'},
                        {label:'大于十年',value:'999'},
                    ]
                } else {
                    this.getXueliPt()
                    this.expList = [
                        {label:'无经验',value:'0'},
                        {label:'一年',value:'1'},
                        {label:'二年',value:'2'},
                        {label:'三年',value:'3'},
                        {label:'四年',value:'4'},
                        {label:'五年',value:'5'},
                        {label:'六年',value:'6'},
                        {label:'七年',value:'7'},
                        {label:'八年',value:'8'},
                        {label:'九年',value:'9'},
                        {label:'十年',value:'10'},
                        {label:'大于十年',value:'999'},
                    ]
                }
            } else {
                this.$Message.error(res.info);
            }
            // console.log(this.expList);
        },
        handleSubmit(name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    editUser(this.formCustom).then(res => {
                        if (res.code == 200) {
                            this.$Message.success(res.info);
                            localStorage.setItem('userImg', this.formCustom.img || 'https://avatars3.githubusercontent.com/u/22117876?s=460&v=4')
                            localStorage.setItem('userName', this.formCustom.name)
                            location.reload()
                        } else {
                            this.$Message.error(res.info);
                        }
                    })
                }
            })
        },
        handleReset(name) {
            this.$refs[name].resetFields();
        }
    }
}
</script>
<style scoped>
.app_pwd {
    background: #fff;
    width: 100%;
    padding: 100px 17% 200px 17%;
}


</style>
