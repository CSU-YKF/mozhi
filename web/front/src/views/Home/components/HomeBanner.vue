<script setup>
import { ref } from 'vue'

const bannerList = ref([])
const imageNames = ['banner1.png', 'banner2.png', 'banner3.png'] 

// 构建图片文件的完整路径并添加到 bannerList 数组
imageNames.forEach(imageName => {
  const imagePath = `../../assets/images/${imageName}` 
  bannerList.value.push(imagePath)
})

</script>



<template>
  <div class="home-banner">
    <el-carousel height="500px">
      <el-carousel-item v-for="item in bannerList" :key="item">
          <img :src="item" alt="">
      </el-carousel-item>
    </el-carousel>
  </div>
</template>



<style scoped lang='scss'>
.home-banner {
  width: 1240px;
  height: 500px;
  position: absolute;
  left: 0;
  top: 0;
  z-index: 98;

  img {
    width: 100%;
    height: 500px;
  }
}
</style>