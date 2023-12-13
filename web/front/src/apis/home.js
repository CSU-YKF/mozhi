import httpInstance from '@/utils/http'


/**
 * @description: 获取我的作品
 * @param {*}
 * @return {*}
 */
export const findNewAPI = () => {
  return httpInstance({
    url: '/home/new'
  })
}

/**
 * @description: 获取热门作品
 * @param {*}
 * @return {*}
 */
export const getHotAPI = () => {
  return httpInstance({
    url: '/home/hot'
  })
}

/**
 * @description: 获取所有作品
 * @param {*}
 * @return {*}
 */
export const getWorksAPI = () => {
  return httpInstance({
    url: '/home/Works'
  })
}