import axios from 'axios';
// import { Notify } from 'quasar';
import router from '@/router/index'

const httpClient = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  }
});

const getAuthToken = () => sessionStorage.getItem('token');

const authInterceptor = (config) => {
  config.headers['Authorization'] = 'Token ' + getAuthToken();
  return config;
}

httpClient.interceptors.request.use(authInterceptor);

const errorInterceptor = error => {
  if (!error.response) {
    // Notify.create('Network/Server error');
    return Promise.reject(error);
  }

  switch (error.response.status) {
    case 400:
      console.error(error.response.status, error.message);
      // Notify.create('Nothing to display', 'Data Not Found');
      break;
    case 401:
      // Notify.create('Please login again', 'Session Expired');
      sessionStorage.removeItem('token');
      router.push('/login');
      break;
    default:
      console.error(error.response.status, error.message);
      // Notify.create('Server Error');
  }
  return Promise.reject(error);
}

const responseInterceptor = response => {
  switch (response.status) {
    case 200:
      break;
    default:
  }
  return response;
}

httpClient.interceptors.response.use(responseInterceptor, errorInterceptor);

export default httpClient;
