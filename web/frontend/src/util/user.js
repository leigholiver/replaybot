import { getUserServers } from "../util/api.js";

export function getToken() {
    return get("user-token");
}

export function setToken(token, callback) {
    set("user-token", token);
    return refreshUserData(callback);
}

export function refreshUserData(callback) {
    return getUserServers().then((data) => {
        setUserData(data);
        callback(data);
    });
}

export function getUserServerById(serverid) {
    return getUserData().servers.filter((server) => server.id === serverid).shift();
}

export function updateServerCache(serverid, data) {
    let userdata = getUserData();
    for(let i=0;i<userdata.servers.length;i++) {
        if(userdata.servers[i].id === serverid) {
            userdata.servers[i].replyTo = data.replyTo;
            userdata.servers[i].listen  = data.listen;
            userdata.servers[i].exclude = data.exclude;
        }
    }
    setUserData(userdata);
}

export function getUserData() {
    return JSON.parse(get("user-data"));
}

export function setUserData(data) {
    set("user-data", JSON.stringify(data));
}

export function logout() {
    localStorage.clear();
}

function get(key) {
    return localStorage.getItem(key);
}

function set(key, data) {
    localStorage.setItem(key, data);
}
