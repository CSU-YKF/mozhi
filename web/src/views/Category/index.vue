<script setup>
import WorksItem from '../Home/components/WorksItem.vue'
import { ref } from 'vue'

const bannerList = ref([])
const imageNames = ['banner1.png', 'banner2.png', 'banner3.png'] 

// 构建图片文件的完整路径并添加到 bannerList 数组
imageNames.forEach(imageName => {
  const imagePath = `../src/assets/images/${imageName}` 
  bannerList.value.push(imagePath)
})


const staticCategoryData = {
  name: '静态分类名称',
  children: [
    {
      id: 1,
      name: '子分类1',
      picture: '../src/assets/images/category1.png',
      works: [
        { id: 1, name: '作品1', price: 10 },
        { id: 2, name: '作品2', price: 15 },
        // 添加更多作品
      ]
    },
    {
      id: 2,
      name: '子分类2',
      picture: '../src/assets/images/category2.png',
      works: [
        { id: 3, name: '作品3', price: 20 },
        { id: 4, name: '作品4', price: 25 },
        // 添加更多作品
      ]
    },
    // 添加更多子分类
  ]
}
</script>

<template>
  <div class="top-category">
    <div class="container m-top-20">
      <!-- 面包屑 -->
      <div class="bread-container">
        <el-breadcrumb separator=">">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>{{ staticCategoryData.name }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
      <!-- 轮播图 -->
      <div class="home-banner">
        <el-carousel height="600px">
          <el-carousel-item v-for="item in bannerList" :key="item">
            <img :src="item" alt="">
          </el-carousel-item>
        </el-carousel>
      </div>
      <div class="sub-list">
        <h3>全部分类</h3>
        <ul>
          <li v-for="i in staticCategoryData.children" :key="i.id">
            <RouterLink :to="`/category/sub/${i.id}`">
              <img :src="i.picture" />
              <p>{{ i.name }}</p>
            </RouterLink>
          </li>
        </ul>
      </div>
      <div class="ref-works" v-for="item in staticCategoryData.children" :key="item.id">
        <div class="head">
          <h3>- {{ item.name }}-</h3>
        </div>
        <div class="body">
          <WorksItem v-for="work in item.works" :works="work" :key="work.id" />
        </div>
      </div>
    </div>
  </div>
</template>



<style scoped lang="scss">
.top-category {
  h3 {
    font-size: 28px;
    color: #666;
    font-weight: normal;
    text-align: center;
    line-height: 100px;
  }

  .sub-list {
    margin-top: 20px;
    background-color: #fff;

    ul {
      display: flex;
      padding: 0 32px;
      flex-wrap: wrap;

      li {
        width: 168px;
        height: 160px;


        a {
          text-align: center;
          display: block;
          font-size: 16px;

          img {
            width: 100px;
            height: 100px;
          }

          p {
            line-height: 40px;
          }

          &:hover {
            color: $xtxColor;
          }
        }
      }
    }
  }

  .ref-works {
    background-color: #fff;
    margin-top: 20px;
    position: relative;

    .head {
      .xtx-more {
        position: absolute;
        top: 20px;
        right: 20px;
      }

      .tag {
        text-align: center;
        color: #999;
        font-size: 20px;
        position: relative;
        top: -20px;
      }
    }

    .body {
      display: flex;
      justify-content: space-around;
      padding: 0 40px 30px;
    }
  }

  .bread-container {
    padding: 25px 0;
  }
}

.home-banner {
  width: 1240px;
  height: 600px;
  margin: 0 auto;


  img {
    width: 100%;
    height: 600px;
  }
}
</style>