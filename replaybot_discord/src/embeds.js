/**
    get embed object from replaydata
    @param author - author from the discord message, username and avatarURL
    @param url - the attachment url
    @param replayData - replay object from replay parsing service
    @return embed data object
**/
function getEmbed(author, message, url, replayData) {
    let teams = [];
    let winners = [];

    replayData.players.forEach(player => {
        if(typeof teams[player['team_id']] === "undefined") {
            teams[player['team_id']] = {
                result: player['result'],
                raceString: "",
                players: []
            };
        }

        teams[player['team_id']]['raceString'] += player['race'][0];

        let p = "";
        if(player['clan'] != null && player['clan'] != "") {
            p += `<${player['clan']}> `;
        }
        let mmr = "";
        if(player['mmr'] > 0) {
            mmr = `- ${player['mmr']} mmr `
        }

        p += `[${player['name']}](${player['profile_url']}) - ${player['race']} ${mmr}- ${player['apm']} apm`;

        teams[player['team_id']]['players'].push(p);
        if(player['result'] == "Win") {
            winners.push(p);
        }        
    });
    
    var teamFields = [];
    teams.forEach((team, i) => {
        let teamString = team.players.join("\n");
        teamFields.push({
            name: `Team ${i+1}`,
            value: teamString
        });
    });
    
    let raceString = teams.filter(a => a.raceString !== "").map(a => a.raceString).join("v");
    let winnerString = winners.join("\n");
    if(winnerString == "") {
        winnerString = "Undecided"
    }
    
    let description = `${message}\n\`${url.split("/").pop()}\``;

    return {
        "embed": {
            author: {
                name: author.username,
                icon_url: author.avatarURL
            },
            title: `${raceString} on ${replayData['map']}`,
            description: description,
            url: url,
            timestamp: new Date(replayData['timeUTC'] * 1000), // unix time to js time
            fields: [
                {
                    name: "Winner",
                    value: `|| ${winnerString} ||`,
                    inline: true
                },
                {
                    name: "Length",
                    value: `|| ${replayData['duration']} ||`,
                    inline: true
                },
                ...teamFields
            ],
            ...defaultEmbed()
        }
    };
}

/**
    get default embed fields (icon, footer, sidebar colour)
    @return embed data object
**/
function defaultEmbed() {
    const { bot_thumbnail, bot_footer_icon, bot_footer_text } = require('./settings.js');
    return {
        // image: { url: bot_thumbnail },
        // thumbnail: { url: bot_thumbnail },
        color: 3447003,
        footer: {
            // icon_url: bot_footer_icon,
            text: bot_footer_text
        }
    }
}

module.exports = {
    getEmbed: getEmbed
};