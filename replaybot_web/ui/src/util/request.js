import axios from 'axios';

export default async function request(baseURL, method, url, data = {}, headers = {}) {
    try {
        const response = await axios({
          method: method,
          url: baseURL + url,
          data: data,
          headers: { "Content-Type": "application/json", ...headers }
        });
        return response.data;
    }
    catch(e) {
        return false;
    }
}