import request from './request.js'
import { getToken as getUserToken } from '../util/userstore.js';
const { apiURL } = require('../api.js');
const cacheTime = 5 * 1000; // ms to cache server responses for

export function getToken(code) {
    return request(apiURL, "POST", "/discord-code?code=" + code);
}

export function getServerJoined(server) {
    return request(apiURL, "GET", `/servers/${server}/joined`);
}

export function getServer(server) {
    let cached = serverCacheGet(server);
    if(cached) {
        return Promise.resolve(cached);
    }
    return request(apiURL, "GET", `/servers/${server}`, null, { 'Authorization': getUserToken() });
}

export function setServer(server, data) {
    return cachedSetServer(
        request(apiURL, "POST", `/servers/${server}/edit`, data, { 'Authorization': getUserToken() })
    );
}

export function setServerMeta(server) {
    return cachedSetServer(
        request(apiURL, "POST", `/servers/${server.id}/edit`, 
            { name: server.name, icon: server.icon }, 
            { 'Authorization': getUserToken() }
        )
    );
}

export function setServerChannels(serverid, channels) {
    return cachedSetServer(
        request(apiURL, "POST", `/servers/${serverid}/edit`, 
            { channels: channels }, 
            { 'Authorization': getUserToken() }
        )
    ); 
}


function cachedSetServer(request) {
    request.then(server => {
        if(server !== false) {
            server['expires'] = Date.now() + cacheTime;
            sessionStorage.setItem(`server_${server.id}`, JSON.stringify(server));
        }
    });
    return request;
}

function serverCacheGet(serverId) {
    let item = sessionStorage.getItem(`server_${serverId}`);
    if(item) {
        item = JSON.parse(item);
        if(item['expires'] > Date.now()) {
            delete item['expires'];
            return item;
        }
    }
    return false;
}

export function filterChannelFields(channels) {
    return channels.filter(channel => channel.type === 0).map(channel => ({ name: channel.name, id: channel.id }))
}

export function getGuildChannels(guildid) {
    return request(apiURL, "GET", `/guilds/${guildid}/channels`, null, { 'Authorization': getUserToken() });
}
