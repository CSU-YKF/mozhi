// import axios from 'axios';
import request from '@/utils/http'
// 处理搜索请求
export const searchWord = ({ word }) => {
  if (!word) {
    // `word` 是空的，不发送请求
    return Promise.reject(new Error('Word is empty'))
  }
  return request({
    url: '/api/v1/search',
    method: 'GET',
    data: {
      word
    }
  })
}