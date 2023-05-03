import service from '@/utils/request'
import axios from 'axios'



export const tonenlizer = (data) =>{
  return service({
    url: '/gpt/tokenlizer',
    donNotShowLoading: true,
    method: 'post',
    data
  })
}


export const tonenlizer_role = (data) =>{
  return service({
    url: '/gpt/tonenlizer_role',
    donNotShowLoading: true,
    method: 'post',
    data
  })
}
