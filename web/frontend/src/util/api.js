import axios from 'axios';
import { getToken } from "./user.js";

const apiURL = process.env.REACT_APP_API_URL;

export function getUserServers(token) {
    return request(apiURL, "GET", "/user-servers");
}

export function getServer(server) {
    return request(apiURL, "GET", `/servers/${server}`);
}

export function setServerConfig(server, data) {
    return request(apiURL, "POST", `/servers/${server}/edit`, {}, {}, data);
}

export function getReplays(server = null, searchTerm = null, cursor = null) {
    const endpoint = searchTerm === null || searchTerm === "" ? "/replays/list" : "/replays/search";
    return request(apiURL, "GET", endpoint, {}, {
        guild:  server? server.id : null,
        query:  searchTerm,
        cursor: cursor
    });
}

async function request(baseURL, method, url, headers = {}, query = {}, data = {}) {
    try {
        const response = await axios({
          method:  method,
          url:     baseURL + url,
          params:  query,
          data:    data,
          headers: { 'Authorization': getToken(), "Content-Type": "application/json", ...headers }
        });
        return response.data;
    }
    catch(e) {
        return false;
    }
}
