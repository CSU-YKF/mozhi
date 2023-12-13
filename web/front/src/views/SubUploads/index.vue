<script setup>
import { searchWord } from '@/apis/search.js'
import { ref } from 'vue'
import { useStore } from '@/stores/wordlist' // 导入 useStore 函数
import { useWorksStore } from '@/stores/works'
import { ElMessage } from 'element-plus'
import 'element-plus/theme-chalk/el-message.css'
import DropDownTag from '@/components/DropDownTagTmp.vue';
import ImgItem from '@/components/ImgTmp.vue';
import { UploadFilled } from '@element-plus/icons-vue'
import { uploadFile } from '@/apis/upload.js';
import 'element-plus/theme-chalk/el-message.css'
import { useRouter } from 'vue-router'
// 提取id的初始化值

const img = useWorksStore()
const isSearchExecuted = ref(false);
const uploadInfo = ref({});
const handleUploadSuccess = async(file) => {
  const responseData = await uploadFile(file)
  // 1. 提示用户
  ElMessage({ type: 'success', message: '上传成功' })
  uploadInfo.value = 
      {
        time: responseData.time,
        score: responseData.score,
        comment: responseData.comment,
        imagePath: responseData.imagePath,
        // tag: [],
      };  
  isSearchExecuted.value = false;
  img.updateWorks(uploadInfo.value);
  }
const searchKeyword = ref('')
const wordlist = ref({})
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
      isSearchExecuted.value = true;
      wordlist.value = {
        wordname: res.wordname,
        wordimgsrc: res.wordimgsrc,
        wordstyle: res.wordstyle
      };
      // 更新全局 store 中的 wordlist
      store.updateWordlist(wordlist.value);
      
      // // 2. 跳转首页
      // router.replace({ path: '/' })
      
    }
const router = useRouter()

const gotoPhotoPage = (image) => {
  const PhotoPageParams = {
    time: image.time,
    score: image.score,
    comment: image.comment,
    imagePath: image.imagePath,
  }

  router.push({ name: 'PhotoPage', params: PhotoPageParams })
}
// console.log('store:', { ...store.getWordlist[0] })
// console.log('works:', img.getWorks[0].imagePath);

const updateImage= () => {
      location.reload();
    }
</script>

<template>
  <div class="container">
    <!-- 面包屑 -->
    <div class="bread-container">
      <el-breadcrumb separator=">">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: `/uploads/search` }">搜索</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="sub-container">
      <!-- 搜索栏 -->
      <div class="search">
        <i class="iconfont icon-search" @click="searchImages"></i>
        <input type="text" v-model="searchKeyword" placeholder="搜搜你想评价的字">
      </div>
    </div>
    <!-- 根据isSearchExecuted的值来决定是否显示el-upload -->
    <el-upload v-if="isSearchExecuted" class="upload-demo" drag :action="uploadAction" multiple :on-success="handleUploadSuccess">
      <el-icon class="el-icon--upload my-upload my-uploadsize"><upload-filled /></el-icon>
      <div class="el-upload__text el-upload__textsize">
        拖拽文件到此处或 <em>点击上传</em>
      </div>
      <template #tip>
        <div class="el-upload__tip el-upload__tipsize">
          支持格式jpg/png文件大小请勿超过500kb。
        </div>
      </template>
    </el-upload>

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
                <button @click="updateImage">Update Image</button>
              </div>
            </div>
            <hr color="#e6ecf0">
           <drop-down-tag v-for="word in store.getWordlist" :key="word.wordname" :tagName="word.wordname">
              <div class="body-leftmargin">
                <div style="display: flex; flex-wrap: wrap;">
                  <img-item class="body-item" v-for="im in img.getWorks" :key="im.time" :value="im.imagePath"
                             :score="im.score" :time="im.time" @click="gotoPhotoPage(im)">
                  </img-item>
                </div>
              </div>
            </drop-down-tag>
          </div>
        </div>
      </div>
      <div style="width: 100%;height: 40px;"></div>
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

.body head {
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
</style>