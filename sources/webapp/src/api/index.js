import axios from 'axios'

export function fetchData(keyword) {
  return axios.get('/search/' + keyword).then(response => { return response.data }).catch(error => { /* console.error(error); */ return Promise.reject(error) })
}
