<script setup>
import { ref } from 'vue'

// 静态的分类数据
const staticCategoryList = [
  {
    name: '整页上传',
  },
  // 添加更多静态数据
]

const categoryList = ref(staticCategoryList)


</script>

<template>
  <ul class="app-header-nav">
    <li class="home">
      <RouterLink to="/index.html">返回首页</RouterLink>
    </li>
    <li class="home" v-for="item in categoryList" :key="item.id">
      <RouterLink active-class="active" to="/uploads/upload">
        {{ item.name }}
      </RouterLink>
    </li>
    <li class="home" >
        <RouterLink active-class="active" to="/uploads/search">搜索上传</RouterLink>
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