
<template>
    <div class="shell-main">
    <div class="container">
    <!-- 面包屑 -->
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
                    <img :src="img.url" alt="" class="images"> <!--图片展示区-->
                </div>
                <div class="body-right">
                    <div class="body-right-item">
                        <div class="item-box">
                            <div class="item-box-info">
                                <div class="body-text1">
                                    <div class="numbers">{{ img.score}}</div>
                                </div>
                            </div>
                        </div>
                        <hr style="margin: 0;" class="shell-main-bottom-bottom">
                    
                        <div class="item-box">
                            <div style="margin: 0 20px;">
                                <div class="body-text2" style="font-weight: bolder;">作品名</div>
                                <br>
                                <div class="body-text2">{{ img.name }}</div>
                            </div>
                        </div>
                        <hr style="margin: 0;" class="shell-main-bottom-bottom">
                        <div class="item-box" >
                            <div style="margin: 0 20px;">
                                <div class="body-text2" style="font-weight: bolder;">AI评价：</div>
                                <br>
                                <div class="body-text2">{{ img.comment }}</div>
                            </div>
                        </div>
                        <hr style="margin: 0;" class="shell-main-bottom-bottom">
                    <!-- <div class="body-right-item">
                        <div class="item-box">
                            <div style="margin: 0 20px;">
                                <div class="body-text1">标签</div>
                                <div class="tag-item">
                                    <div class="tag" v-for="imgtag in img.tag" :key="imgtag.tno">{{ imgtag.tname }}</div>
                                    <div class="tag" style="background-color: #fb7299;">pink</div>
                                    <div class="tag" style="background-color: #dd001b;">red</div>
                                </div>
                            </div>
                        </div>
                    </div> -->
                    <div class="body-right-item">
                        <div class="item-box">
                            <div style="margin: 0 20px;">
                                <button class="body-text1 button" @click="$router.go(-1)">返回</button>
                            </div>
                            <hr style="margin: 0;" >
                        </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>
    </div>
    
    <!-- <div class="shell-main-footer">
                    <span>linkin</span>
                </div> -->

</template>

<script>

export default {
    
    props: ['name', 'score', 'comment', 'imagePath'],
    computed: {
        img() {
        return {
            url: this.imagePath,
            score: this.score,
            name: this.name, // 如果你有一个名为 'name' 的路由参数，你应该在这里使用它
            comment: this.comment
        }
        }
    },

}
</script>

<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

.numbers {
  font-size: 108px;
  color: #ff9b04;
  font-family: 'Roboto', sans-serif;
}
.bread-container {
  padding: 25px 0;
  color: #666;
}
.body-main {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 20px;
    height: 100vh; 
    
}

.body-left {
    display: flex;
    flex-direction: column;
    margin: 0 15px 15px 15px;
    align-items: center;
    /* width: 60%; */
}

@media screen and (width >=1385px) {
    .body-right {
        width: 500px;

    }
}

@media screen and (width < 1385px){
    .body-right {
        width: 800px;

    }
}

/* @media screen and (width < 840px) {
    .body-right {
        width: 97%;

    }
} */

@media screen and (width >=1385px) {
    .comment-postion {
        position: relative;
        right: 250px;
    }

}
@media screen and (width < 1385px) {
    .comment-postion {
        position: relative;
    }

}

.margin-twin {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
}



.body-right-item {
    width: 100%;
    min-height: 100px;
    margin-top: 20px;
    background-color: white;
    border-radius: 6px;
    overflow: hidden;
}

.item-box {
    width: 100%;
    min-height: 80px;
    margin: 20px 0;
    display: flex;
    flex-direction: row;
    align-items: center;
   // position: relative; /* 或者 absolute、fixed、sticky */
    z-index: 2;
    overflow: auto;

}

.item-box-info {
    margin: 0 20px;
    width: calc(100% - 40px);
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow-wrap: break-word; 
    word-wrap: break-word;
}

.body-text1 {
    text-align: left;
    font-size: 20px;
    font-weight: bolder;
    line-break: anywhere;
    position: relative; /* 或者 absolute、fixed、sticky */
    z-index: 2;
    transform: scale(1.2);
    display: flex;
    justify-content: center;
    align-items: center;
}

.body-text2 {
    text-align: left;
    font-weight: 100;
    font-size: 15px;
    font-family: 微软雅黑;
    position: relative; /* 或者 absolute、fixed、sticky */
    z-index: 2;
    //transform: scale(1.2);
    overflow-wrap: break-word; 
    word-wrap: break-word;
}
.button {
    background-color: #8ddff8; /* 设置背景色为蓝色 */
    color: white; /* 设置文字颜色为白色 */
    border: none; /* 移除边框 */
    padding: 10px 20px; /* 设置内边距 */
    text-align: center; /* 文字居中 */
    text-decoration: none; /* 移除下划线 */
    display: inline-block; /* 使得元素可以设置宽度和高度 */
    font-size: 16px; /* 设置字体大小 */
    margin: 4px 2px; /* 设置外边距 */
    cursor: pointer; /* 鼠标悬停时变为手形 */
}
.button:hover {
  background-color: white;
  color: black;
}
.images {
            width: 350px;
            height: 450px;
            column-count: 4;
            column-gap: 20px;
            margin-top: 20px;
            margin-right: 30px;
            position: relative;
            margin-bottom: 15px;
            overflow: hidden;
            border: #000 solid 2px;
            transition: .3s;
            opacity: 0.9;
            padding: 5px;
   
        }
.images::before{
    content: '';
    position: absolute;
    left: 50%;
    transform: translate(-50%);
    height: 100%;
    width: 500px;
    background-image: linear-gradient(to bottom, #a1e6ff, #a8ffe2, #a1e6ff);
    z-index: 0;
}
.images:hover {
    transform: scale(1.05);
    opacity: 1;
}

body .shell-main {
    width: 100%;
    height: auto;
    position: relative;
    transition: .2s;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 100px;
}

body .shell-main::before {
    content: '';
    width: 250px;
    height: 100%;
    background-image: linear-gradient(to bottom, #a1e6ff, #a8ffe2, #a1e6ff);
    position: absolute;
    transform: translate(-130%, 0);
    z-index: 0;
    bottom: 0;
    opacity: 0.7;
    
}

body .shell-main::after {
  content: '';
  width: 250px;
  height: 100%;
  background-image: linear-gradient(to right, #a1e6ff 0%, #a8ffe2 50%, transparent 50%, transparent 100%);
  background-size: 90px 100%;
  position: absolute;
  transform: translate(355%);
  z-index: 0;
  opacity: 0.7;
  
}
body .shell-main-bottom-bottom::before {
    content: '';
    width: 250px;
    height: 250px;
    border: 20px solid rgba(0, 255, 255, 0.167);
    position: absolute;
    border-radius: 10px;
    right: 250px;
    top: 50px;
    transform: rotate(30deg) translate(-50%, -50%);
    animation: transform 4s infinite;
    opacity: 0.8;
    z-index: 0;
    animation: transform 4s infinite;
    @keyframes transform {
        0% {
            transform: rotate(30deg) translate(0);
        }

        50% {
            transform: rotate(40deg) translate(10px);
        }

        100% {
            transform: rotate(30deg) translate(0px);
        }
    }
}

body .shell-main-header-left::before {
    content: '';
    width: 250px;
    height: 250px;
    border: 20px solid rgba(0, 255, 255, 0.3);
    position: absolute;
    bottom: 50px;
    left: 50px;
    border-radius: 10px;
    transform: rotate(30deg);
    animation: transform 4s infinite;
    @keyframes transform {
        0% {
            transform: rotate(30deg) translate(0);
        }
    
        50% {
            transform: rotate(40deg) translate(10px);
        }
    
        100% {
            transform: rotate(30deg) translate(0px);
        }
    }
}

 

</style>