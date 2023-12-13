// wordlist.js
import { defineStore } from 'pinia';

export const useStore = defineStore({
  id: 'store',
  state: () => ({
    data: {
      wordlist: [
        {
          wordname: '111',
          wordimgsrc: '2',
          wordstyle: '33',
        },
      ],
      
    },
  }),
  actions: {
    updateWordlist(newWordlist) {
      this.data.wordlist = [...newWordlist];
    },
  },
  getters: {
    getWordlist: (state) => state.data.wordlist,
  },
});

// 导出 useStore 实例
export function setupStore() {
  return useStore();
}
