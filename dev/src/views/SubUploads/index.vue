<script setup>
import { searchWord } from '@/apis/search.js'
import { ref } from 'vue'
import { useStore } from '@/stores/wordlist' // 导入 useStore 函数
import { ElMessage } from 'element-plus'
import 'element-plus/theme-chalk/el-message.css'
// import { useRouter } from 'vue-router'

const searchKeyword = ref('')
const wordlist = ref([])
// const router = useRouter()
const store = useStore() // 使用 useStore 函数创建 store 实例
const searchImages = async () => {
      const keyword = searchKeyword.value.trim()

      if (!keyword) {
        // 关键词是空的，不发送请求
        ElMessage({ type: 'error', message: '请输入搜索关键词' })
        return
      }
      const res = await searchWord( {word : keyword} )
      // 1. 提示用户
      ElMessage({ type: 'success', message: '搜索成功' })
      wordlist.value = 
      {
        wordname: res.wordname,
        wordimgsrc: res.wordimgsrc,
        wordstyle: res.wordstyle
      };
      // 更新全局 store 中的 wordlist
      store.updateWordlist(wordlist.value);
      // // 2. 跳转首页
      // router.replace({ path: '/' })
    }

</script>


<template>
  <div class="container">
    <!-- 面包屑 -->
    <div class="bread-container">
      <el-breadcrumb separator=">">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: `/uploads/search` }">搜索
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="sub-container">
      <!-- 搜索栏 -->
      <div class="search">
        <i class="iconfont icon-search" @click="searchImages"></i>
        <input type="text" v-model="searchKeyword" placeholder="搜搜你想评价的字">
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

  .search {
    width: 170px;
    height: 32px;
    position: relative;
    border-bottom: 1px solid #e7e7e7;
    line-height: 32px;

    .icon-search {
      font-size: 18px;
      margin-left: 5px;
    }

    input {
      width: 120px;
      padding-left: 5px;
      color: #666;
    }
  }


}
</style>