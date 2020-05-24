const axios = require('axios');

function store(rep) {
    let data = {
        url: rep.url,
        replayData: rep.replayData,
        message: rep.message.content + "\n",
        source: {
            author: {
                id: rep.message.author.id,
                name: rep.message.author.username,
                avatar: rep.message.author.avatar
            },
            channel: {
                id: rep.message.channel.id,
                name: rep.message.channel.name
            },
            guild: {
                id: rep.message.channel.guild.id,
                name: rep.message.channel.guild.name,
                icon: rep.message.channel.guild.icon
            }
        }
    }
    return request("POST", `/servers/${rep.message.channel.guild.id}/store`, data);
}

function getServer(server) {
    return request("GET", `/servers/${server}`);
}

function join(server) {
    return request("POST", `/join/${server}`);
}

function leave(server) {
    return request("POST", `/leave/${server}`);
}

async function request(method, url, data = null, headers = {}) {
    headers = { 
        "Content-Type": "application/json", 
        "X-Replaybot-Token": process.env.BOT_SHARED_KEY,
        ...headers 
    }
    try {
        const response = await axios({
          method: method,
          url: process.env.API_ENDPOINT + url,
          data: data,
          headers: headers
        });
        return response.data;
    }
    catch(e) {
        console.log(e);
        return false;
    }
}

module.exports = {
    store: store,
    getServer: getServer,
    join: join,
    leave: leave
}