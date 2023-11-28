<script setup>
import { ref } from 'vue';
// import WorksItem from '../Home/components/WorksItem.vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { uploadFile } from '@/apis/upload.js';
import { ElMessage } from 'element-plus'
import 'element-plus/theme-chalk/el-message.css'

// 提取id的初始化值
const initialId = 0;

const uploadInfo = ref({
  id: initialId,
  score: '',
  comment: ''
});

// const uploadAction = ref('http://127.0.0.1:4523/m1/2767929-0-default/api/v1/img/upload');

const handleUploadSuccess = async(file) => {
  const responseData = await uploadFile(file)
  // 1. 提示用户
  ElMessage({ type: 'success', message: '上传成功' })
  uploadInfo.value.id++;

  // 只有在上传成功后，设置score和comment
  uploadInfo.value.score = responseData.score;
  uploadInfo.value.comment = responseData.comment;
  }

// const handleUploadSuccess = async (response, file) => {
//   const responseData = await uploadFile(file.raw);
//   console.log('Server Response:', responseData);
  
//   // 增加id，确保每次都是唯一的
//   uploadInfo.value.id++;
  
//   // 只有在上传成功后，设置score和comment
//   uploadInfo.value.score = responseData.score;
//   uploadInfo.value.comment = responseData.comment;
// }

</script>

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
          :action="uploadAction"
          multiple
          :on-success="handleUploadSuccess"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            拖拽文件到此处或 <em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持格式jpg/png文件大小请勿超过500kb。
            </div>
          </template>
        </el-upload>
        <div class="uploaded-images">
          <p>id: {{ uploadInfo.id }}</p>
          <p>Score: {{ uploadInfo.score }}</p>
          <p>Comment: {{ uploadInfo.comment }}</p>
        </div>
      </div>
      <!-- <div class="sub-list">
        <h3>全部分类</h3>
        <ul>
          <li v-for="i in staticWordData.children" :key="i.id">
            <RouterLink :to="`/uploads/words/${i.id}`">
              <img :src="i.picture" />
              <p>{{ i.name }}</p>
            </RouterLink>
          </li>
        </ul>
      </div>
      <div class="ref-works" v-for="item in staticWordData.children" :key="item.id">
        <div class="head">
          <h3>- {{ item.name }}-</h3>
        </div>
        <div class="body">
          <WorksItem v-for="work in item.works" :works="work" :key="work.id" />
        </div>
      </div> -->
    </div>
  </div>
</template>



<style scoped lang="scss">
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