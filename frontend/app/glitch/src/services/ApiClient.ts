import axios, { type AxiosInstance } from 'axios'

const api_client: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-type': 'application/json'
  }
})

export default api_client
