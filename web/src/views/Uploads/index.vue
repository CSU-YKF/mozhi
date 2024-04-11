<template>
  <div class="top-word">
    <div class="container m-top-20">
      <!-- 面包屑 -->
      <div class="bread-container">
        <el-breadcrumb separator=">">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>上传</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
      <div>
        <el-upload
          class="upload-demo"
          drag
          action="#"
          multiple
          :http-request="uploadRequest"
          :on-success="handleUploadSuccess"
        >
          <el-icon class="el-icon--upload my-upload my-uploadsize">
            <upload-filled />
          </el-icon>
          <div class="el-upload__text el-upload__textsize">
            拖拽文件到此处或 <em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip el-upload__tipsize">
              支持格式jpg/png文件大小请勿超过500kb。
            </div>
          </template>
        </el-upload>
        <div class="uploaded-images"></div>
      </div>
      <div class="body">
        <div class="main-body">
          <!--画作展示栏-->
          <div class="body-box2">
            <div class="body-leftmargin">
              <div class="body-nav">
                <div class="body-nav-item text2">作品</div>
              </div>
              <hr color="#e6ecf0" />
              <drop-down-tag tagName="识别结果">
                <div class="body-leftmargin">
                  <div style="display: flex; flex-wrap: wrap">
                    <img-item
                      class="body-item"
                      v-for="im in img.getWorks"
                      :key="im.id"
                      :value="im.imagePath"
                      :id="im.id"
                      :score="im.score"
                      :name="im.name"
                      @click="gotoPhotoPage(im)"
                    >
                    </img-item>
                  </div>
                </div>
              </drop-down-tag>
            </div>
            <div id="lineChartBox">
              <canvas id="lineChart"></canvas>
            </div>
          </div>
        </div>
        <div style="width: 100%; height: 40px"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { UploadFilled } from '@element-plus/icons-vue';
import { ElMessage, ElLoading } from 'element-plus';
import 'element-plus/theme-chalk/el-message.css';
import { useRouter } from 'vue-router';
import { useWorksStore } from '@/stores/holeworks';
import ImgItem from '@/components/ImgTmp.vue';
import DropDownTag from '@/components/DropDownTagTmp.vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Chart } from 'chart.js/auto';

const urlRoot = 'http://43.139.115.247:8080';

const img = useWorksStore();
const chartCanvas = ref(null);
let chartInstance = null;
let loadingInstance = null;

// 初始化
const init = () => {
  chartCanvas.value = document.getElementById('lineChart');
  const ctx = chartCanvas.value.getContext('2d');
  chartInstance = new Chart(ctx, config);
  if (Cookies.get('token') === undefined) {
    newToken();
    updateImage();
  } else {
    axios
      .get(urlRoot + '/verify?token=' + Cookies.get('token'))
      .catch((error) => {
        console.log(error);
        newToken();
      })
      .finally(() => {
        updateImage();
      });
  }
};

// 获取新的令牌
const newToken = () => {
  axios
    .get(urlRoot + '/getToken')
    .then((response) => {
      Cookies.set('token', response.data, { expires: 999 });
    })
    .catch((error) => {
      console.log(error);
    });
};

// 上传请求配置
const uploadConfig = {
  headers: {
    'Content-Type': 'multipart/form-data',
  },
};

// 发送上传请求
const uploadRequest = (request) => {
  console.log(request);
  loadingInstance = ElLoading.service({ text: '正在生成评价,请耐心等待...' });
  axios
    .post(urlRoot + '/upload', { image: request.file }, uploadConfig)
    .then((response) => {
      console.log(response);
      ElMessage({ type: 'success', message: '评价生成成功' });
      updateImage();
    })
    .catch((error) => {
      console.log(error);
      ElMessage({ type: 'error', message: '上传失败,请重试' });
    })
    .finally(() => {
      if (loadingInstance) {
        loadingInstance.close();
      }
    });
};

// 上传成功后自动更新图片列表
const handleUploadSuccess = () => {
  updateImage();
};

// 更新图片列表
const updateImage = () => {
  axios
    .get(urlRoot + '/queryAll')
    .then((response) => {
      const data = response.data;
      let works = [];
      for (let i = 0; i < data.length; i++) {
        works.push({
          id: data[i].id,
          name: data[i].charName,
          score: data[i].score,
          comment: data[i].comment,
          imagePath: urlRoot + '/getImage?id=' + data[i].id,
          date: new Date(data[i].uploadDate),
        });
      }
      img.setWorks(works);
    })
    .catch((error) => {
      console.log(error);
    })
    .finally(() => {
      updateChart();
    });
};

// 图表配置
const config = {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      {
        label: '分数',
        data: [],
        borderColor: 'teal',
        fill: false,
        hidden: false,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: '分数统计',
      },
    },
    interaction: {
      intersect: false,
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: '日期',
        },
      },
      y: {
        display: true,
        title: {
          display: true,
          text: '分数',
        },
        suggestedMin: 0,
        suggestedMax: 10,
      },
    },
  },
};

// 更新图表
const updateChart = () => {
  if (img.works.length < 3) {
    return;
  }
  let labels = [];
  let data = [];
  for (let i = 2; i < img.works.length; i++) {
    labels.push(
      img.works[i].date.getMonth() + 1 + '月' + img.works[i].date.getDate() + '日'
    );
    data.push(img.works[i].score);
  }
  chartInstance.data.labels = labels;
  chartInstance.data.datasets[0].data = data;
  chartInstance.update();
};

const router = useRouter();

const gotoPhotoPage = (image) => {
  const PhotoPageParams = {
    id: image.id,
    name: image.name,
    score: image.score,
    comment: image.comment,
    imagePath: image.imagePath,
    date: image.date,
  };

  router.push({ name: 'PhotoPage', params: PhotoPageParams });
};

onMounted(() => {
  init();
});
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
.top-word {
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

  .my-upload {
    height: 300px;
    border-radius: 10px;
    margin: 20px 40px 20px 40px;
  }

  .my-uploadsize {
    font-size: 180px;
  }

  .el-upload__tipsize {
    font-size: 14px;
    color: #999;
  }

  .el-upload__textsize {
    font-size: 28px;
    color: #999;
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

.body head {
  margin: 0;
  padding: 0;
}

.body {
  width: 100%;
  min-height: 1000px;
  background-color: #f7f7f7;
}

/*页面主体样式*/
.main-body {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/*页面主体公告栏样式*/
.body-box1 {
  width: 90%;
  min-height: 150px;
  background-color: white;
  border-radius: 6px;
  margin-top: 60px;
}

/*页面主体画作展示样式*/
.body-box2 {
  width: 90%;
  min-height: 600px;
  background-color: white;
  border-radius: 6px;
  margin-top: 60px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

/*页面主体两边间隔样式*/
.body-leftmargin {
  margin: 0 10px;
}

/*页面主体导航栏样式*/
.body-nav {
  width: 100%;
  height: 60px;
  margin: 2px;
  display: flex;
  flex-direction: row;
  align-items: center;
}

/*页面主体导航栏盒子样式*/
.body-nav-item {
  margin: 0 10px;
  overflow: hidden;
  color: #777;
}

.body-nav-item:hover {
  color: #000;
}

/*页面主体内容样式*/
.body-item {
  display: flex;
  flex-wrap: wrap;
}

/*页面主体图片样式*/
.body-img {
  width: 200px;
  height: 200px;
  object-fit: cover;
}

/*页面主体图片盒子样式*/
.img-item {
  width: 200px;
  height: 200px;
  overflow: hidden;
  border-radius: 12px;
  border: 2px solid #000;
  box-shadow: 0 0 5px #000;
  margin-left: 20px;
  margin-top: 20px;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.2);
  }
}

/*头部导航栏文字*/
.text1 {
  font-size: 20px;
  font-weight: bolder;
  color: #000;
}

/*主体导航栏文字*/
.text2 {
  font-size: 18px;
  font-family: 微软雅黑;
  color: #777777;
}

.text3 {
  font-size: 22px;
  font-family: 微软雅黑;
  font-weight: bolder;
  color: #000;
}

.hover-div {
  background-color: #ccc;
  padding: 10px;
  position: absolute;
  top: 20px;
  left: 20px;
}

/*页面主体悬浮菜单样式*/
.body-content {
  position: absolute;
  width: 200px;
  height: 200px;
  border-radius: 12px;
  z-index: 2;
  background-color: white;
  opacity: 0.8;
  transition: all 0.3s ease;

  &:hover {
    opacity: 1;
  }
}

/*页面主体悬浮菜单文字样式*/
.body-content-text {
  margin: 2px;
  color: #000;
  font-size: 16px;
  font-weight: bold;
}

.on-body-content-show {
  display: flex;
  align-items: center;
  justify-content: center;
}

.on-body-content-hide {
  display: none;
}

.drop-down-arrow {
  font-size: 14px;
  margin-left: 10px;
}

.drop-down-tag {
  display: flex;
  min-height: 60px;
  flex-direction: column;
  justify-content: center;
}

.tag-bar {
  display: flex;
  align-items: center;
  margin: 15px 0;
}
</style>