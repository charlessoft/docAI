import service from '@/utils/request'
import axios from 'axios'


export const testRole = (data) => {
  return service({
    url: '/gpt/testrole',
    donNotShowLoading: true,
    method: 'post',
    data
  })
}

export const querySimilarity = (data) => {
  return service({
    url: '/gpt/querysimilarity',
    donNotShowLoading: true,
    method: 'post',
    data
  })
}


export const memerychat_raw = (data) =>{
  return service({
    url: '/gpt/memerychat_raw',
    donNotShowLoading: true,
    method: 'post',
    data
  })
}
