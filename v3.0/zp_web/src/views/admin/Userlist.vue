<template>
    <div class="app_data">
        <div class="title_data">
            <h2>用户管理</h2>
        </div>
        <div class="query-c">
            <Form inline>
                <Button type="primary" @click="addRow()"
                >新增
                </Button
                >
                <FormItem prop="user">
                    <Input type="text" v-model="pageInfo.name" placeholder="姓名">
                    </Input>
                </FormItem>
                <FormItem prop="user">
                    <Input type="text" v-model="pageInfo.phone" placeholder="手机号码">
                    </Input>
                </FormItem>
                <FormItem>
                    <Button type="primary" @click="handleSubmit('formInline')"
                    >搜索
                    </Button
                    >
                </FormItem>
            </Form>
        </div>
        <div class="update">
            <Table border :columns="columns1" :data="data1">
                <template #caozuo="{ row, index }">
                    <Button type="primary" size="small" @click="editRow(row)"
                    >编辑
                    </Button
                    >
                    <Button type="info" size="small" @click="chongzhi(row)"
                    >重置密码
                    </Button
                    >
                    <Button type="success" size="small" @click="startUser(row.id)" v-if="row.login_flag == '0'"
                    >启用
                    </Button
                    >
                    <Button type="warning" size="small" @click="stopUser(row.id)" v-else
                    >停用
                    </Button
                    >
                    <Button type="error" size="small" @click="remove(row.id)"
                    >删除
                    </Button
                    >
                </template>
            </Table>
            <div class="page">
                <Page :total="pageInfo.total" @on-change="ChangePage" show-total/>
            </div>
        </div>
        <!-- 删除提示框 -->
        <Modal
            v-model="modal"
            title="提示"
            :loading="loading"
            @on-ok="asyncOK">
            <p>确定要删除吗</p>
        </Modal>
        <!-- 启用提示框 -->
        <Modal
            v-model="modalStart"
            title="提示"
            :loading="loading"
            @on-ok="asyncStart">
            <p>确定要启用吗</p>
        </Modal>
        <!-- 停用提示框 -->
        <Modal
            v-model="modalStop"
            title="提示"
            :loading="loading"
            @on-ok="asyncStop">
            <p>确定要停用吗</p>
        </Modal>
        <!-- 编辑弹窗 -->
        <Modal
            v-model="isedit"
            title="编辑"
            :z-index="10000"
            @on-ok="handleEdit"
            @on-cancel="isedit = false"
        >
            <Form
                ref="uploadForm"
                :model="isedit"
                :rules="ruleValidate"
                :label-width="80"
            >
                <FormItem label="姓名" prop="name">
                    <Input v-model="uploadForm.name" placeholder="请输入姓名"/>
                </FormItem>
                <FormItem label="邮箱" prop="email">
                    <Input v-model="uploadForm.email" placeholder="请输入邮箱"/>
                </FormItem>
                <FormItem label="电话号码" prop="phone">
                    <Input v-model="uploadForm.phone" placeholder="请输入电话号码"/>
                </FormItem>
                <FormItem label="角色" prop="role">
                    <Select v-model="uploadForm.role" placeholder="请选择 ">
                        <Option value="2">普通用户</Option>
                        <Option value="3">特殊用户</Option>
                        <Option value="1">管理员</Option>
                    </Select>
                </FormItem>
                <FormItem label="备注" prop="remarks">
                    <Input v-model="uploadForm.remarks" type="textarea" placeholder="请输入备注"/>
                </FormItem>
            </Form>
            <div slot="footer">
                <Button type="text" @click="canal">取消</Button>
                <Button type="primary" @click="handleEdit">确定</Button>
            </div>
        </Modal>
        <!-- 新增弹窗 -->
        <Modal
            v-model="isAdd"
            title="新增"
            :z-index="10000"
            @on-ok="handleAdd"
            @on-cancel="isAdd = false"
        >
            <Form
                :model="addForm"
                :label-width="80"
            >
                <FormItem label="账号" prop="account">
                    <Input v-model="addForm.account" placeholder="请输入账号"/>
                </FormItem>
                <FormItem label="姓名" prop="name">
                    <Input v-model="addForm.name" placeholder="请输入姓名"/>
                </FormItem>
                <FormItem label="邮箱" prop="email">
                    <Input v-model="addForm.email" placeholder="请输入邮箱"/>
                </FormItem>
                <FormItem label="电话号码" prop="phone">
                    <Input v-model="addForm.phone" placeholder="请输入电话号码"/>
                </FormItem>
                <FormItem label="角色" prop="role">
                    <Select v-model="addForm.role" placeholder="请选择 ">
                        <Option value="2">普通用户</Option>
                        <Option value="3">特殊用户</Option>
                        <Option value="1">管理员</Option>
                    </Select>
                </FormItem>
                <FormItem label="备注" prop="remarks">
                    <Input v-model="addForm.remarks" type="textarea" placeholder="请输入备注"/>
                </FormItem>
            </Form>
            <div slot="footer">
                <Button type="text" @click="canal">取消</Button>
                <Button type="primary" @click="handleAdd">确定</Button>
            </div>
        </Modal>

    </div>
</template>
<script>
import {delUser, getUsers, startUser, stopUser, editUser, addUser ,chongzhi} from "@/api";

export default {
    data() {
        return {
            pageInfo: {
                pageNo: 1,
                pageSize: 10,
                total: 0,
                phone: "",
                name: "",
            },
            columns1: [
                {
                    title: "姓名",
                    key: "name",
                    align: "center",
                },
                {
                    title: "账号",
                    key: "account",
                    align: "center",
                },
                {
                    title: "邮箱",
                    key: "email",
                    align: "center",
                },
                {
                    title: "电话号码",
                    key: "phone",
                    align: "center",
                },
                {
                    title: "状态",
                    key: "login_flag",
                    align: "center",
                    render: (h, params) => {
                        let isconfirm = params.row.login_flag;
                        if (isconfirm == '0') {
                            return h(
                                "span",
                                {
                                    style: {
                                        color: "red",
                                    },
                                },
                                "停用"
                            );
                        } else {
                            return h("span", {
                                style: {
                                    color: "#19be6b",
                                },
                            }, "启用");
                        }
                    },
                },
                {
                    title: "角色",
                    key: "role",
                    align: "center",
                    render: (h, params) => {
                        let isconfirm = params.row.role;
                        if (isconfirm == '1') {
                            return h("span", {
                            }, "管理员");
                        } else if (isconfirm == '2'){
                            return h("span", {
                            }, "普通用户");
                        } else {
                            return h("span", {
                            }, "特殊用户");
                        }
                    },
                },
                {
                    title: "操作",
                    slot: "caozuo",
                    align: "center",
                    width: 300,
                },
            ],
            data1: [],
            modal: false,
            modalStop: false,
            modalStart: false,
            loading: true,
            id: '',
            //编辑
            isedit: false,
            uploadForm: {
                name: "",
                email: "",
                phone: "",
                role: "",
                remarks: "",
            },
            // 新增
            isAdd: false,
            addForm: {
                account: "",
                name: "",
                email: "",
                phone: "",
                role: "",
                remarks: "",
            },
            ruleValidate: {
                name: [{required: true, message: "姓名不能为空", trigger: "blur"}],
                email: [
                    {required: true, message: "邮箱不能为空", trigger: "blur"},
                ],
                phone: [
                    {required: true, message: "电话号码不能为空", trigger: "blur"},
                ],
                role: [{required: true, message: "角色不能为空", trigger: "blur"}],
            },
        };
    },
    mounted() {
        this.init();
    },
    methods: {
        // 重置密码
        async chongzhi(e) {
            const {data:res} = await chongzhi(`id=${e.id}`);
            if (res.code == 200) {
                this.$Message.success(res.info);
                this.init()
            } else {
                this.$Message.error(res.info);
            }
        },
        // 新增
        addRow() {
            this.isAdd = true;
        },
        // 新增提交
        async handleAdd() {
            if (!this.addForm.account) {
                this.$Message.error("请输入账号");
                return false
            }
            if (!this.addForm.name) {
                this.$Message.error("请输入姓名");
                return false
            }
            if (!this.addForm.email) {
                this.$Message.error("请输入邮箱");
                return false
            }
            if (!this.addForm.phone) {
                this.$Message.error("请输入电话号码");
                return false
            }
            addUser(this.addForm).then(res => {
                const result = res.data
                if (result.code == 200) {
                    this.$Message.success(result.info);
                    this.init()
                    this.isAdd = false
                } else {
                    this.$Message.error(result.info);
                }
            })
        },
        // 编辑
        editRow(row, index) {
            this.isedit = true;
            this.uploadForm = row;
        },
        // 编辑提交
        async handleEdit(uploadForm) {
            if (!this.uploadForm.name) {
                this.$Message.error("请输入姓名");
                return false
            }
            if (!this.uploadForm.email) {
                this.$Message.error("请输入邮箱");
                return false
            }
            if (!this.uploadForm.phone) {
                this.$Message.error("请输入电话号码");
                return false
            }
            editUser(this.uploadForm).then(res => {
                const result = res.data
                if (result.code == 200) {
                    this.$Message.success(result.info);
                    this.init()
                    this.isedit = false
                } else {
                    this.$Message.error(result.info);
                }
            })
        },

        // 取消编辑
        canal() {
            this.isedit = false
            this.isAdd = false
            this.init()
        },

        // 搜索
        handleSubmit() {
            this.init();
        },
        // 获取数据
        async init() {
            const {data:res} = await getUsers(
                `pageNo=${this.pageInfo.pageNo}&pageSize=${this.pageInfo.pageSize}&name=${this.pageInfo.name}&phone=${this.pageInfo.phone}`
            );
            this.pageInfo.total = res.total;
            this.pageInfo.pageNo = res.pageno;
            this.pageInfo.pageSize = res.pagesize;
            this.data1 = res.info;
        },
        // 翻页
        ChangePage(e) {
            this.pageInfo.pageNo = e;
            this.init();
        },
        openInfo(e) {
            window.open(e);
        },
        // 删除
        remove(e) {
            this.id = e
            this.modal = true
        },
        async asyncOK() {
            this.modal = false;
            const {data:res} = await delUser(`id=${this.id}`);
            if (res.code == 200) {
                this.$Message.success(res.info);
                this.init()
            } else {
                this.$Message.error(res.info);
            }
        },
        // 启用
        startUser(e) {
            this.id = e
            this.modalStart = true
        },
        async asyncStart() {
            this.modalStart = false;
            const {data:res} = await startUser(`id=${this.id}`);
            if (res.code == 200) {
                this.$Message.success(res.info);
                this.init()
            } else {
                this.$Message.error(res.info);
            }
        },
        // 停用
        stopUser(e) {
            this.id = e
            this.modalStop = true
        },
        async asyncStop() {
            this.modalStop = false;
            const {data:res} = await stopUser(`id=${this.id}`);
            if (res.code == 200) {
                this.$Message.success(res.info);
                this.init()
            } else {
                this.$Message.error(res.info);
            }
        }
    },
};
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

[type=reset], [type=submit], button, html [type=button] {
    -webkit-appearance: button;
    margin-right: 5px;
}
</style>
