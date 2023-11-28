<script setup>
import LayoutHeaderUl from './LayoutHeaderUl.vue'
import { ref } from 'vue'
import { useStore } from '@/stores/wordlist' // 导入 useStore 函数
import { ElMessage } from 'element-plus'
import 'element-plus/theme-chalk/el-message.css'
import { searchWord } from '@/apis/search.js'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchKeyword = ref('')
const wordlist = ref([])
// const router = useRouter()
const store = useStore() // 使用 useStore 函数创建 store 实例
const SearchImages = async () => {
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
      
      router.replace({ path: '/uploads/upload' })
    }
</script>

<template>
  <header class='app-header'>
    <div class="container">
      <h1 class="Mozhilogo">
        <RouterLink to="/">墨智</RouterLink>
      </h1>

      <LayoutHeaderUl />
      <div class="search">
        <i class="iconfont icon-search" @click="SearchImages"></i>
        <input type="text" v-model="searchKeyword" placeholder="搜搜你想评价的字">
      </div>
    </div>
</header>
</template>


<style scoped lang='scss'>
.app-header {
  background: #fff;

  .container {
    display: flex;
    align-items: center;
  }

  .Mozhilogo {
    width: 300px;

    a {
      display: block;
      margin-left: 60px;
      height: 90px;
      width: 120px;
      text-indent: -9999px;
      background: url('@/assets/images/Mozhilogo.png') no-repeat center 10px / contain;
    }
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

  .cart {
    width: 50px;

    .curr {
      height: 32px;
      line-height: 32px;
      text-align: center;
      position: relative;
      display: block;

      .icon-cart {
        font-size: 22px;
      }

      em {
        font-style: normal;
        position: absolute;
        right: 0;
        top: 0;
        padding: 1px 6px;
        line-height: 1;
        background: $helpColor;
        color: #fff;
        font-size: 12px;
        border-radius: 10px;
        font-family: Arial;
      }
    }
  }
}
</style>