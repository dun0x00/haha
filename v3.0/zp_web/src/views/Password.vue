<template>
    <div class="app_pwd">
        <div class="form">
            <Form ref="formCustom" :model="formCustom" :rules="ruleCustom" :label-width="80">
                <FormItem label="用户姓名:" prop="name">
                    <span class="fn-style">{{ formCustom.name }}</span>
                </FormItem>
                <FormItem label="登录账号:" prop="account">
                    <span class="fn-style">{{ formCustom.account }}</span>
                </FormItem>
                <FormItem label="原始密码:" prop="oldPwd">
                    <Input type="password" v-model="formCustom.oldPwd"></Input>
                </FormItem>
                <FormItem label="新密码:" prop="newPwd">
                    <Input type="password" v-model="formCustom.newPwd"></Input>
                </FormItem>
                <FormItem label="密码确认:" prop="newPwdCheck">
                    <Input type="password" v-model="formCustom.newPwdCheck"></Input>
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
import {changePwd} from "@/api";
import {resetTokenAndClearUser} from "../utils";
export default {
    data () {
        const validateOld = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入旧密码'));
            } else {
                callback();
            }
        };
        const validatePassCheck = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入新密码'));
            } else {
                callback();
            }
        };
        const validateAge = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('请输入新密码确认'));
            }else{
                callback();
            }
        };

        return {
            formCustom: {
                name:localStorage.getItem('userName')||'',
                account:localStorage.getItem('account') || '',
                oldPwd: '',
                newPwd:'',
                newPwdCheck:''
            },
            ruleCustom: {
                oldPwd: [
                    { validator: validateOld, trigger: 'blur' }
                ],
                newPwd: [
                    { validator: validatePassCheck, trigger: 'blur' }
                ],
                newPwdCheck: [
                    { validator: validateAge, trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
         handleSubmit (name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    if (this.formCustom.newPwd != this.formCustom.newPwdCheck) {
                        this.$Message.warning('两次密码输入不一致!');
                        return
                    } else {
                        this.change()
                    }
                }
            })
        },
        async change(){
            const {data:res} = await changePwd(`account=${this.formCustom.account}&oldPwd=${this.formCustom.oldPwd}&newPwd=${this.formCustom.newPwd}`)
            // console.log(res);
            if(res.code == 200){
                this.$Message.success(res.info+ '  请重新登录！');
                resetTokenAndClearUser()
                this.$router.push({ name: 'data' })
            } else {
                this.$Message.error(res.info);
            }
        },
        handleReset (name) {
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
