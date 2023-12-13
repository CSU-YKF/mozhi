// // uploadApi.js
// import axios from 'axios';

// export async function uploadFile(file) {
//   const formData = new FormData();
//   formData.append('file', file);

//   const response = await axios.post(
//     'http://127.0.0.1:4523/m1/2767929-0-default/api/v1/img/upload',
//     formData
//   );

//   return response.data; // 返回服务器响应的JSON数据
// }
// import axios from 'axios';
import request from '@/utils/http'
// import { useUserStore } from '@/stores/userStore'
// const userStore = useUserStore()

// 处理搜索请求
export const uploadFile = ({ file }) => {
  // if (!userStore.userInfo.token) {
  //   return  request({
  //     url: '/api/v1/public/img/upload',
  //     method: 'POST',
  //     data: {
  //       file
  //     }
  //   })
  // }
  return request({
    url: '/api/v1/img/upload',
    method: 'POST',
    data: {
      file
    }
  })
}