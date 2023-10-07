<script setup>
import LayoutHeaderUl from './LayoutHeaderUl.vue'
</script>

<template>
  <header class='app-header'>
    <div class="container">
      <h1 class="Mozhilogo">
        <RouterLink to="/">墨智</RouterLink>
      </h1>

      <LayoutHeaderUl />
      <div class="search">
        <i class="iconfont icon-search"></i>
        <input type="text" placeholder="搜一搜">
      </div>
    </div>S
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