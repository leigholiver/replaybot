const baseURL            = "https://discordapp.com/api"
const cdnURL             = "https://cdn.discordapp.com"
const clientID           = process.env.REACT_APP_CLIENT_ID;
const redirectURI        = process.env.REACT_APP_REDIRECT_URI;

// for the auth window
var objWindow = null;
var objWindowURL = null;

export function getAvatarURLFromUser(user) {
    return `${cdnURL}/avatars/${user['id']}/${user['avatar']}.png`;
}

export function getAvatarURLFromGuild(guild) {
    if(guild['icon'] === null) return null;
    return `${cdnURL}/icons/${guild['id']}/${guild['icon']}.png`;
}

export function getLoginURL() {
    return `${baseURL}/oauth2/authorize?client_id=${clientID}&redirect_uri=${encodeURIComponent(redirectURI)}&response_type=code&scope=identify%20guilds`
}

export function guildAuthWindow(serverid) {
    let url = getGuildAuthURL(serverid);
    if(objWindow == null || objWindow.closed || url !== objWindowURL) {
        objWindow = window.open(url, "Discord Authentication", "width=600,height=900,left=650,top=90,resizable=yes,scrollbars=yes,status=yes");
        objWindowURL = url;
        var timer = setInterval(function() { 
            if(objWindow.closed) {
                clearInterval(timer);
                window.location.href=`/servers/${serverid}`
            }
        }, 1000);
    }
    objWindow.focus();
}

function getGuildAuthURL(serverid) {
    return `${baseURL}/oauth2/authorize?client_id=${clientID}&permissions=83968&redirect_uri=${encodeURIComponent(redirectURI)}&scope=bot&guild_id=${serverid}`
}