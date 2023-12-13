// createRouter：创建router实例对象
// createWebHistory：创建history模式的路由

import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login/index.vue'
import Layout from '@/views/Layout/index.vue'
import Uploads from '@/views/Uploads/index.vue'
import SubUploads from '@/views/SubUploads/index.vue' 
import Register from '@/views/Register/index.vue'
import index from '@/views/newhome/index.vue'
import PhotoPage from '@/views/PhotoPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  // path和component对应关系的位置
  routes: [
    {
      path: '/',
      redirect: '/index.html', // 重定向到/index.html
      meta: {
        // 在这里设置自定义的meta字段
        pageRefreshed: false, // 默认为false
      },
    },
    {
      path: '/index.html',
      component: index
    },
    {    
          path: '/',
          component: Layout, 
          children: [
            {
              path: 'uploads/search',
              component: SubUploads
            },
            {
              path: 'uploads/upload',
              component: Uploads
            },
            ]
      },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/register',
      component: Register
    },
    {
      path: '/PhotoPage/:time/:score/:comment/:imagePath',
      name: 'PhotoPage',
      component: PhotoPage,
      props: true
    }
  ],
  // 路由滚动行为定制
  scrollBehavior () {
    return {
      top: 0
    }
  }
})


export default router