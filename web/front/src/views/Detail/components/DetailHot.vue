
<script setup>
import { computed } from 'vue'
import { ref } from 'vue'

// 设计props参数 适配不同的title和数据
const props = defineProps({
  hotType: {
    type: Number
  }
})

// 适配title 1 - 24小时热榜  2-周热榜
const TYPEMAP = {
  1: '24小时热榜',
  2: '周热榜'
}
const title = computed(() => TYPEMAP[props.hotType])

// 静态的热门商品数据，用于替代 API 数据
const staticHotList = [
  {
    id: 1,
    picture: '/static/images/product1.jpg',
    name: '商品1',
    desc: '商品描述1',
    price: 100
  },
  {
    id: 2,
    picture: '/static/images/product2.jpg',
    name: '商品2',
    desc: '商品描述2',
    price: 150
  },
  // 添加更多静态数据
]

const hotList = ref(staticHotList)
</script>

<template>
  <div class="works-hot">
    <h3>{{ title }}</h3>
    <!-- 商品区块 -->
    <RouterLink to="/" class="works-item" v-for="item in hotList" :key="item.id">
      <img :src="item.picture" alt="" />
      <p class="name ellipsis">{{ item.name }}</p>
      <p class="desc ellipsis">{{ item.desc }}</p>
      <p class="price">&yen;{{ item.price }}</p>
    </RouterLink>
  </div>
</template>


<style scoped lang="scss">
.works-hot {
  h3 {
    height: 70px;
    background: $helpColor;
    color: #fff;
    font-size: 18px;
    line-height: 70px;
    padding-left: 25px;
    margin-bottom: 10px;
    font-weight: normal;
  }

  .works-item {
    display: block;
    padding: 20px 30px;
    text-align: center;
    background: #fff;

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
}
</style>