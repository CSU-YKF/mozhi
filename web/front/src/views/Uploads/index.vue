<script setup>
import { ref } from 'vue';
// import WorksItem from '../Home/components/WorksItem.vue'
import { UploadFilled } from '@element-plus/icons-vue'
// import { uploadFile } from '@/apis/upload.js';
import { ElMessage } from 'element-plus'
import 'element-plus/theme-chalk/el-message.css'
import { useRouter } from 'vue-router'
import { useWorksStore } from '@/stores/holeworks'
import ImgItem from '@/components/ImgTmp.vue';
import DropDownTag from '@/components/DropDownTagTmp.vue';

//const uploadUrl = 'http://127.0.0.1:4523/m1/2767929-0-default/api/v1/img/upload'
//http://43.139.115.247:9999/api/v1/public/img/upload
//http://127.0.0.1:4523/m1/2767929-0-default/api/v1/img/upload
const uploadAction = ref('http://43.139.115.247:9999/api/v1/public/img/upload');
const img = useWorksStore()
const isSearchExecuted = ref(false);
const uploadInfo = ref({});
// const handleUploadSuccess = async(file) => {
//   const responseData = await uploadFile(file)
//   console.log('Server Response:', responseData);
//   // 1. 提示用户
//   ElMessage({ type: 'success', message: '上传成功' })
//   uploadInfo.value = 
//       {
//         name: responseData.name,
//         score: responseData.score,
//         comment: responseData.comment,
//         imagePath: responseData.imagePath,
//         // tag: [],
//       };  
//   isSearchExecuted.value = false;
//   img.updateWorks(uploadInfo.value);
//   }

const  handleUploadSuccess = async(response, file, fileList)=> {
    console.log(response); // 打印服务器的响应
    console.log(file);
    console.log(fileList);
    console.log(response.image_id);
    //const responseData = await uploadFile(response.image_id)
    //console.log(responseData);
    // 在这里处理服务器的响应
    //   // 1. 提示用户
    ElMessage({ type: 'success', message: '上传成功' })
    uploadInfo.value = 
        {
          name: file.name,
          score: response.score,
          comment: response.comment,
          imagePath: 'http://43.139.115.247:9999/api/v1/public/img/get?id='+response.image_id,
        };  
    isSearchExecuted.value = false;
    img.updateWorks(uploadInfo.value);
    }


const router = useRouter()

const gotoPhotoPage = (image) => {
  const PhotoPageParams = {
    name: image.name,
    score: image.score,
    comment: image.comment,
    imagePath: image.imagePath,
  }

  router.push({ name: 'PhotoPage', params: PhotoPageParams })
}

const  updateImage= () => {
      location.reload();
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
          <el-icon class="el-icon--upload my-upload my-uploadsize"><upload-filled /></el-icon>
          <div class="el-upload__text el-upload__textsize">
            拖拽文件到此处或 <em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip el-upload__tipsize" >
              支持格式jpg/png文件大小请勿超过500kb。
            </div>
          </template>
        </el-upload>
        <div class="uploaded-images">
        </div>
      </div>
      <div class="body">
      <div class="main-body">
        <!--画作展示栏-->
        <div class="body-box2">
          <div class="body-leftmargin">
            <div class="body-nav">
              <div class="body-nav-item text2">
                作品
              </div>
              <div>
                <button class="update-button" @click="updateImage">Update Image</button>
              </div>
            </div>
            <hr color="#e6ecf0">
           <drop-down-tag tagName="识别结果">
              <div class="body-leftmargin">
                <div style="display: flex; flex-wrap: wrap;">
                  <img-item class="body-item" v-for="im in img.getWorks" :key="im.name" :value="im.imagePath"
                             :score="im.score" :name="im.name" @click="gotoPhotoPage(im)">
                  </img-item>
                </div>
              </div>
            </drop-down-tag>
          </div>
        </div>
      </div>
      <div style="width: 100%;height: 40px;"></div>
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
  .my-upload {
  height: 300px; /* 你的高度 */
  border-radius: 10px; /* 你的圆角 */
  margin: 20px 40px 20px 40px;  /* 你的外边距 */
  }
  .my-uploadsize {
  font-size: 180px; /* 你的图标大小 */
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
}.body head {
  margin: 0;
  padding: 0;
}

.body {
  width: 100%;
  min-height: 1000px;
  background-color: #e6ecf0;
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
  /* border: 1px solid #000; */
}

.body-nav-item:hover {
  color: #eead6d;
}

/*页面主体内容样式*/
.body-item {
  display: flex;
  flex-wrap: warp;
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
  border: 2px solid #eb972a;
  box-shadow: 0 0 5px #eb972a;
  margin-left: 20px;
  margin-top: 20px;
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
}

/*页面主体悬浮菜单文字样式*/
.body-content-text {
  margin: 2px;
  color: #fb7299;
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

.update-button {
  background-color: #8ddff8;
  color: white;
  border: none;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  transition-duration: 0.4s;
  cursor: pointer;
}

.update-button:hover {
  background-color: white;
  color: black;
}
</style>