import service from '@/utils/request'
import axios from 'axios'



export const getcopuslist = (data) => {
  return service({
    url: '/gpt/getcorpuslist',
    method: 'get',
    data
  })
}

export const delcorpus = (id) =>{
  return service({
    url: '/gpt/delcorpus',
    method: 'post',
    data
  })
}

export const delcorpusIds = (data) => {
  return service({
    url: '/gpt/delcorpusIds',
    method: 'post',
    data
  })
}
