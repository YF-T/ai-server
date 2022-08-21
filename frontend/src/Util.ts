import axios from 'axios'


export const request = (path: string, param: FormData): Promise<any> => {
    return axios
    .post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})  
  }


