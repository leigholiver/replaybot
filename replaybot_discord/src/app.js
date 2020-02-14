const { join, leave, store, getServer } = require('./api.js');
const { getEmbed } = require('./embeds.js');
const { isSC2Replay, getReplayMetadata } = require('./replays.js');

const Discord = require('discord.js');
const client = new Discord.Client();

var servers = [];
var timer = null;

client.on('ready', () => {
    // poll the discord client to see when we join/leave servers
    timer = setInterval(serverChanges, 1000);
    console.log(`Connected as ${client.user.tag}`);
});

client.on('disconnect', () => {
    clearInterval(timer);
    console.log(`Disconnected`);
});

client.on('message', message => {
    if (message.attachments.size > 0) {
        message.attachments.forEach(attachment => {
            if(isSC2Replay(attachment.url)) {
                getServer(message.guild.id).then(server => {
                    if((server.listen.length == 0 || server.listen.includes(message.channel.id))
                        && !server.exclude.includes(message.channel.id)) {
                        
                        let channel = message.channel;
                        if(server.replyTo != "reply") {
                            channel = message.guild.channels.get(server.replyTo);
                        }
                        postEmbed(channel, message, attachment, (message, attachment, replayData) => {
                            store({
                                url: attachment.url,
                                replayData: replayData,
                                message: message
                            });
                        });
                    }
                })
                .catch(() => {
                    // couldn't reach the web service - default to basic reply mode
                    postEmbed(message.channel, message, attachment, (message, attachment, replayData) => {});
                });
            }
        });
    }
});

/*
    do the thing
*/ 
function postEmbed(channel, message, attachment, callback) {
    getReplayMetadata(attachment.url).then( replayData => {
        if(!replayData) {
            console.error(`Error parsing replay at ${attachment.url}`)
            return;
        }
        channel.send(getEmbed(message.author, message.content, attachment.url, replayData));
        callback(message, attachment, replayData);
    });
}

/* notify the web service that we have joined or left a server */
function serverChanges() {
    let newServers = [...client.guilds.values()];

    newServers.filter(item => !servers.includes(item)).forEach(item => {
        join(item.id);
        console.log(`Joined ${item.id} ${item.name}`)
    });

    servers.filter(item => !newServers.includes(item)).forEach(item => {
        leave(item.id);
        console.log(`Left ${item.id} ${item.name}`)
    });

    servers = newServers;
}

client.login(process.env.DISCORD_TOKEN);