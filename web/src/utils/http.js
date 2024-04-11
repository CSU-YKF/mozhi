//axios封装
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const http = axios.create({
  //baseURL: 'http://127.0.0.1:4523/m1/2767929-0-default',
  baseURL: 'http://43.139.115.247:9999',
  timeout: 5000
})

// axios请求拦截器
http.interceptors.request.use(config => {
  return config
}, e => Promise.reject(e))

// axios响应式拦截器
http.interceptors.response.use(res => res.data, e => {
  ElMessage({
    type: 'error',
    message: e.response.data.message 
  })  
  return Promise.reject(e)
})


export default http