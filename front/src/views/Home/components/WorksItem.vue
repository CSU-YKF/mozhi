<script setup>
defineProps({
  works: {
    tppe: Object,
    default: () => { }
  }
})
</script>


<template>
  <RouterLink to="/" class="works-item">
    <img v-img-lazy="works.picture" alt="" />
    <p class="name ellipsis">{{ works.name }}</p>
    <p class="desc ellipsis">{{ works.desc }}</p>
    <p class="price">&yen;{{ works.price }}</p>
  </RouterLink>
</template>

<style lang="scss" scoped>
.works-item {
  display: block;
  width: 220px;
  padding: 20px 30px;
  text-align: center;
  transition: all .5s;

  &:hover {
    transform: translate3d(0, -3px, 0);
    box-shadow: 0 3px 8px rgb(0 0 0 / 20%);
  }

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
</style>