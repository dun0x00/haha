import { resetRouter } from '@/router'

export function resetTokenAndClearUser() {
    // 退出登陆 清除用户资料
    localStorage.setItem('token', '')
    localStorage.setItem('userImg', '')
    localStorage.setItem('userName', '')
    localStorage.setItem('account', '')
    localStorage.setItem('role', '')
    localStorage.setItem('userId', '')
    // 登陆成功 假设这里是后台返回的 token
    localStorage.setItem('token', '')
    // 重设路由
    resetRouter()
}

export const defaultDocumentTitle = '招聘信息可视化系统'
export function getDocumentTitle(pageTitle) {
    if (pageTitle) return `${defaultDocumentTitle} - ${pageTitle}`
    return `${defaultDocumentTitle}`
}
