// works.js
import { defineStore } from 'pinia';

export const useWorksStore = defineStore({
  id: 'works',
  state: () => ({
    works: [
      {
        name: '示例1:德',
        score: '7.72',
        comment: '书法作品笔力雄健，结构疏密有致，但笔画略显生硬，未见韵律。',
        imagePath: '/src/assets/images/exp1.png',
        // tags: ['标签1'],
      },
      {
        name: '示例2:仁',
        score: '8.8',
        comment: '笔画简洁流畅，结构均衡。',
        imagePath: '/src/assets/images/exp2.png',
        // tags: ['标签1'],
      },
    ],
  }),
  actions: {
    updateWorks(newWorks) {
      this.works.push(newWorks);
    },
  },
  getters: {
    getWorks: (state) => state.works,
  },
});

// 导出 useWorksStore 实例
export function setupStore() {
  return useWorksStore();
}
