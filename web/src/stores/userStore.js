// 管理用户数据相关

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { loginAPI } from '@/apis/login'
export const useUserStore = defineStore('user', () => {
  // 1. 定义管理用户数据的state
  const userInfo = ref({})
  // 2. 定义获取接口数据的action函数
  const getUserInfo = async ({ account, password }) => {
    const res = await loginAPI({ account, password })
    console.log(res)  // 打印出 res 对象
    if (res) {
      userInfo.value = res
      userInfo.value.token = true 
    } else {
      console.error('res is undefined')
    }
  }

  // 退出时清除用户信息
  const clearUserInfo = () => {
    userInfo.value = {}
    userInfo.value.token = ''
  }
  // 3. 以对象的格式把state和action return
  return {
    userInfo,
    getUserInfo,
    clearUserInfo
  }
}
, {
  persist: true,
})