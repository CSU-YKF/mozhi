src/views/Home.vue

<template>
    <div>
      <div v-html="externalHtml"></div>
    </div>
  </template>
  
  <script>
  export default {
    created() {
    // 判断是否是首次访问
    if (!sessionStorage.getItem('visited')) {
      // 避开全局插件的加载逻辑
      window.location.href = '/index.html';
    }},
    data() {
      return {
        externalHtml: '', // 存储加载的 HTML 内容
      };
    },
    mounted() {
      this.loadExternalHtml();
    },
    methods: {
      async loadExternalHtml() {
        try {
          const response = await fetch('/index.html'); // 路径根据实际情况调整
          this.externalHtml = await response.text();
        } catch (error) {
          console.error('Failed to load external HTML:', error);
        }
      },
    },
  };
  </script>
  
  <style>
  /* 这里放你的 CSS 样式 */
  </style>
<!--   
<script>
export default {
  data() {
    return {
      externalHtml: '', // 存储加载的 HTML 内容
    };
  },
  mounted() {
    this.loadExternalHtml();
  },
  methods: {
    async loadExternalHtml() {
      try {
        const response = await fetch('/index.html'); // 路径根据实际情况调整
        this.externalHtml = await response.text();
        this.executeScripts(); // 执行脚本
      } catch (error) {
        console.error('Failed to load external HTML:', error);
      }
    },
    executeScripts() {
      // 执行脚本
      const scripts = document.querySelectorAll('script');
      scripts.forEach((script) => {
        const newScript = document.createElement('script');
        newScript.text = script.text;
        document.body.appendChild(newScript).parentNode.removeChild(newScript);
      });
    },
  },
};
</script> -->
