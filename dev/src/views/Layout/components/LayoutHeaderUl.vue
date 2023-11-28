<script setup>
import { ref } from 'vue'
import { useStore } from '@/stores/wordlist'
// 获取存储实例
const store = useStore()
// 静态的分类数据
const staticCategoryList = [
  {
    id: 1,
    name: '分类',
  },
  // 添加更多静态数据
]

const categoryList = ref(staticCategoryList)


</script>

<template>
  <ul class="app-header-nav">
    <li class="home">
      <RouterLink to="/">首页</RouterLink>
    </li>
    <li class="home" v-for="item in categoryList" :key="item.id">
      <RouterLink active-class="active" :to="`/category/${item.id}`">
        {{ item.name }}
      </RouterLink>
    </li>
    <li class="home" v-for="item in store.data.wordlist" :key="item.wordname">
      <!-- 上传标签 -->
      <template v-if="item.wordstyle === 'search'">
        <RouterLink active-class="active" to="/uploads/search">{{ item.wordname }}</RouterLink>
      </template>
      <!-- 搜索结果标签 -->
      <template v-else>
        <RouterLink
          active-class="active"
          :to="`/uploads/upload`"
        >{{ item.wordname }}</RouterLink>
      </template>
    </li>
  </ul>
</template>



<style lang="scss">
.app-header-nav {
  width: 820px;
  display: flex;
  padding-left: 40px;
  position: relative;
  z-index: 998;

  li {
    margin-right: 40px;
    width: 38px;
    text-align: center;

    a {
      font-size: 16px;
      line-height: 32px;
      height: 32px;
      display: inline-block;

      &:hover {
        color: $xtxColor;
        border-bottom: 1px solid $xtxColor;
      }
    }

    .active {
      color: $xtxColor;
      border-bottom: 1px solid $xtxColor;
    }
  }
}
</style>