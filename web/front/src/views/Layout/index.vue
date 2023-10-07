<script setup>
import LayoutNav from './components/LayoutNav.vue'
import LayoutHeader from './components/LayoutHeader.vue'
import LayoutFooter from './components/LayoutFooter.vue'
import LayoutFixed from './components/LayoutFixed.vue'
import { ref, onMounted } from 'vue'

// 静态的分类数据
const staticCategoryList = [
  {
    id: 1,
    name: '分类',
    children: [
      { id: 11, name: '子分类1' },
      { id: 12, name: '子分类2' }
    ],
    works: [
      { id: 101, name: '作品1', desc: '作品描述1', price: 100, picture: '图片路径1' },
      { id: 102, name: '作品2', desc: '作品描述2', price: 150, picture: '图片路径2' }
    ]
  }
  // 添加更多静态数据
]

// 使用静态数据替代实际的数据
const categoryData = ref(staticCategoryList)

onMounted(() => {
  return () => categoryData 
})
</script>

<template>
  <LayoutFixed />
  <LayoutNav />
  <LayoutHeader />
  <!-- 添加key 破坏复用机制 强制销毁重建 -->
  <!-- <RouterView :key="$route.fullPath" /> -->
  <RouterView />
  <LayoutFooter />
</template>