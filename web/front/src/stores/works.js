// works.js
import { defineStore } from 'pinia';

export const useWorksStore = defineStore({
  id: 'works',
  state: () => ({
    works: [
      {
        name: '示例1',
        score: '9.6',
        comment: '示例1的评论',
        imagePath: '/src/assets/images/xiaoguo1.jfif',
        // tags: ['标签1'],
      },
      {
        name: '示例3',
        score: '9.2',
        comment: '示例2的评论',
        imagePath: '/src/assets/images/xiaoguo2.jpg',
        // tags: ['标签1'],
      },
      {
        name: '示例3',
        score: '9.4',
        comment: '示例3的评论',
        imagePath: '/src/assets/images/xiaoguo3.jfif',
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
