<template>
  <div class="shell-main">
    <div class="container">
      <!-- 面包屑导航 -->
      <div class="bread-container">
        <el-breadcrumb separator=">">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item :to="{ path: `/uploads/search` }">搜索</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
    </div>

    <div class="body">
      <div class="body-main">
        <div class="shell-main-header">
          <div class="margin-twin">
            <div class="body-left shell-main-header-left">
              <el-card :body-style="{ padding: '0px' }" class="image-card">
                <img :src="img.url" alt="" class="images" />
              </el-card>
            </div>
            <div class="body-right">
              <div class="body-right-item">
                <el-card>
                  <div class="item-box">
                    <div class="item-box-info">
                      <div class="body-text1">
                        <div class="numbers">{{ Number(img.score).toFixed(1) }}</div>
                      </div>
                    </div>
                  </div>
                </el-card>
              </div>

              <div class="body-right-item">
                <el-card>
                  <div class="item-box">
                    <div style="margin: 0 20px;">
                      <div class="body-text2" style="font-weight: bolder;">作品名</div>
                      <br />
                      <div class="body-text2">{{ img.name }}</div>
                    </div>
                  </div>
                </el-card>
              </div>

              <div class="body-right-item">
                <el-card>
                  <div class="item-box">
                    <div style="margin: 0 20px;">
                      <div class="body-text2" style="font-weight: bolder;">AI评价</div>
                      <br />
                      <div class="body-text2">{{ img.comment }}</div>
                    </div>
                  </div>
                </el-card>
              </div>

              <div class="body-right-item">
                <el-card>
                  <div class="item-box">
                    <div style="margin: 0 20px;">
                      <div class="body-text2" style="font-weight: bolder;">关于 "{{ char }}"</div>
                      <br />
                      <div class="body-text2" id="char-info" v-html="basicDom + meaningDom"></div>
                    </div>
                  </div>
                </el-card>
              </div>

              <div class="body-right-item">
                <el-card>
                  <div class="item-box">
                    <div style="margin: 0 20px;">
                      <el-button type="primary" @click="goBack">返回</el-button>
<!--                      <el-button type="success" @click="uploadImage">上传图片</el-button>-->
                    </div>
                  </div>
                </el-card>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();

    const id = ref(route.params.id);
    const name = ref(route.params.name);
    const score = ref(route.params.score);
    const comment = ref(route.params.comment);
    const imagePath = ref(route.params.imagePath);
    const date = ref(route.params.date);

    const img = computed(() => ({
      id: id.value,
      url: imagePath.value,
      score: score.value,
      name: name.value,
      comment: comment.value,
      date: date.value,
    }));

    const char = ref('');
    const basicDom = ref('');
    const meaningDom = ref('');

    onMounted(() => {
      if (Number(id.value) === -1) {
        char.value = '德';
      } else if (Number(id.value) === -2) {
        char.value = '仁';
      } else {
        char.value = name.value;
      }

      fetchCharInfo();
    });

    const fetchCharInfo = () => {
      axios
        .get(`http://localhost:8080/getInformation/${char.value}`)
        .then((response) => {
          basicDom.value = response.data.basicDom;
          meaningDom.value = response.data.meaningDom;
        })
        .catch((error) => {
          console.error('获取字符信息时发生错误:', error);
        });
    };

    const goBack = () => {
      router.go(-1);
    };

    const uploadImage = () => {
      // 实现上传图片的逻辑
      // ...
    };

    return {
      img,
      char,
      basicDom,
      meaningDom,
      goBack,
      uploadImage,
    };
  },
};
</script>

<style lang="scss">
// 全局样式
body {
  background-color: #f0f0f0;
  font-family: '微软雅黑', sans-serif;
}

// ElementUI 样式覆盖
.el-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  transition: all 0.3s ease;

  &:hover {
    box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.2);
  }

  .el-card__body {
    padding: 20px;
  }
}

.el-button {
  border-radius: 20px;
  font-weight: bold;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
  }

  &.el-button--primary {
    background-color: #1c1c1c;
    border-color: #1c1c1c;

    &:hover {
      background-color: #000;
      border-color: #000;
    }
  }

  &.el-button--success {
    background-color: #28803d;
    border-color: #28803d;

    &:hover {
      background-color: #1e6b30;
      border-color: #1e6b30;
    }
  }
}
</style>

<style lang="scss" scoped>
.shell-main {
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.bread-container {
  margin-bottom: 20px;
}

.body-main {
  display: flex;
  flex-direction: column;
}

.margin-twin {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.body-left {
  flex: 1;
  margin-right: 20px;
}

.body-right {
  flex: 1;
}

.image-card {
  border-radius: 10px;
  overflow: hidden;

  .images {
    width: 100%;
    height: auto;
    object-fit: cover;
    transition: transform 0.3s ease;

    &:hover {
      transform: scale(1.05);
    }
  }
}

.numbers {
  font-size: 48px;
  font-weight: bold;
  color: #1c1c1c;
}

.body-text1 {
  font-size: 24px;
  font-weight: bold;
  color: #1c1c1c;
  margin-bottom: 10px;
}

.body-text2 {
  font-size: 16px;
  color: #666;
  line-height: 1.6;
}

#char-info {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 10px;
  background-color: #f8f8f8;
}
</style>