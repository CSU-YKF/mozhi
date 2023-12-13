// works.js
import { defineStore } from 'pinia';

export const useWorksStore = defineStore({
  id: 'works',
  state: () => ({
    works: [
      {
        time: 2023.11,
        score: '91',
        comment: '这是测试2',
        imagePath: '/src/assets/images/works3.jpg',
        // tags: ['标签1'],
      },
      {
        time: 2023.11,
        score: '11',
        comment: '这是测试2',
        imagePath: '/src/assets/images/works4.jpg',
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
