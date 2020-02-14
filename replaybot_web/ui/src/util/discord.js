import request from './request.js'
const { clientID, redirectURI } = require('../api.js');
const baseURL = "https://discordapp.com/api"
const cdnURL = "https://cdn.discordapp.com"

// for the auth window
var objWindow = null;
var objWindowURL = null;

/**
{
  avatar: "26c8bfe4f39b32c594fce8d60d249683",​
  discriminator: "9673",​
  flags: 0,​
  id: "95462775685394432",​
  locale: "en-US",​
  mfa_enabled: false,​
  username: "tn"
}
**/
export function getUser(access_token) {
    return request(baseURL, "GET", "/users/@me", undefined, {
        Authorization: "Bearer " + access_token,
        "content-type": "application/json"
    });
}

/**
{
  "id": "80351110224678912",
  "name": "1337 Krew",
  "icon": "8342729096ea3675442027381ff50dfe",
  "owner": true,
  "permissions": 36953089
}
**/
export function getUserServers(access_token) {
    return request(baseURL, "GET", "/users/@me/guilds", undefined, {
        Authorization: "Bearer " + access_token,
        "content-type": "application/json"
    });
}

/* filter servers by those the user has permission to add the bot to */
export function getUserAdminServers(servers) {
    return servers.filter(server => {
        return server['owner'] === true || 
            (server['permissions'] & 0x00000008) === 0x00000008 || // ADMINISTRATOR
            (server['permissions'] & 0x00000020) === 0x00000020    // MANAGE_GUILD
    });

}

/* URL Functions */
export function getAvatarURLFromUser(user) {
    return `${cdnURL}/avatars/${user['id']}/${user['avatar']}.png`;
}

export function getAvatarURLFromGuild(guild) {
    return `${cdnURL}/icons/${guild['id']}/${guild['icon']}.png`;
}

export function getGuildAuthURL(serverid) {
    return `${baseURL}/oauth2/authorize?client_id=${clientID}&permissions=83968&redirect_uri=${encodeURIComponent(redirectURI)}&scope=bot&guild_id=${serverid}`
}

export function getLoginURL() {
    return `${baseURL}/oauth2/authorize?client_id=${clientID}&redirect_uri=${encodeURIComponent(redirectURI)}&response_type=code&scope=identify%20guilds`
}

export function authWindow(serverid) {
    let url = getGuildAuthURL(serverid);
    if(objWindow == null || objWindow.closed || url !== objWindowURL) {
        objWindow = window.open(url, "Discord Auth", "width=600,height=900,left=650,top=90,resizable=yes,scrollbars=yes,status=yes");
        objWindowURL = url;
        var timer = setInterval(function() { 
            if(objWindow.closed) {
                clearInterval(timer);
                window.location.href=`/servers/${serverid}`

                // fires same event whether success or not
                // guess we redirect to the server page and 
                // error if the bot hasnt joined
            }
        }, 1000);
    }
    objWindow.focus();
}