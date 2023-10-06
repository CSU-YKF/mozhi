<script setup>
import WorksItem from '../Home/components/WorksItem.vue'
import { ref } from 'vue' 

// 静态的面包屑导航数据
const staticCategoryData = {
  parentId: 1,
  parentName: '父分类',
  name: '子分类'
}

// 静态的商品列表数据
const staticWorkList = [
  {
    id: 1,
    name: '商品1',
    desc: '商品描述1',
    price: 100
  },
  {
    id: 2,
    name: '商品2',
    desc: '商品描述2',
    price: 150
  },
  // 添加更多静态数据
]

const categoryData = ref(staticCategoryData)
const workList = ref(staticWorkList)

// 在这里你可以继续添加其他静态数据，或者将它们替换为你需要的实际数据。
// 请确保静态数据的结构与实际数据的结构相匹配。

</script>

<template>
  <div class="container">
    <!-- 面包屑 -->
    <div class="bread-container">
      <el-breadcrumb separator=">">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: `/category/${categoryData.parentId}` }">{{ categoryData.parentName }}
        </el-breadcrumb-item>
        <el-breadcrumb-item>{{ categoryData.name }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="sub-container">
      <!-- 商品列表 -->
      <div class="body">
        <WorksItem v-for="works in workList" :works="works" :key="works.id" />
      </div>
    </div>
  </div>
</template>



<style lang="scss" scoped>
.bread-container {
  padding: 25px 0;
  color: #666;
}

.sub-container {
  padding: 20px 10px;
  background-color: #fff;

  .body {
    display: flex;
    flex-wrap: wrap;
    padding: 0 10px;
  }

  .works-item {
    display: block;
    width: 220px;
    margin-right: 20px;
    padding: 20px 30px;
    text-align: center;

    img {
      width: 160px;
      height: 160px;
    }

    p {
      padding-top: 10px;
    }

    .name {
      font-size: 16px;
    }

    .desc {
      color: #999;
      height: 29px;
    }

    .price {
      color: $priceColor;
      font-size: 20px;
    }
  }

  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }


}
</style>