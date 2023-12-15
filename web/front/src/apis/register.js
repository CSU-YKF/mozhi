import request from '@/utils/http'

export const register = ({ account, password }) => {
  return request({
    url: '/register',
    method: 'POST',
    data: {
      account,
      password
    }
  })
}