import { defineStore } from 'pinia';
import { reactive, toRefs } from 'vue';

export const useStore = defineStore({
  id: 'store',
  state: () => ({
    data: {
      wordlist: [
        {
          wordname: '上传',
          wordimgsrc: '',
          wordstyle: 'search',
        }
      ],
    },
  }),
  actions: {
    updateWordlist(newWordlist) {
      this.data.wordlist.push(newWordlist);
      this.data = reactive(this.data); // 更新 data 触发响应式
    },
  },
  getters: {
    getWordlist: (state) => toRefs(state.data).wordlist,
  },
});

// 导出 useStore 实例
export function setupStore() {
  return useStore();
}