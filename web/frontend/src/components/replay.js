import React from 'react';

import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import GetAppIcon from '@material-ui/icons/GetApp';

import { SmallAvatar } from './smallavatar.js';
import TimeSince from '../util/TimeSince';
import ButtonPopover from '../components/material-ui/button-popover.js';
import { getAvatarURLFromUser, getAvatarURLFromGuild } from '../util/discord.js';

const useStyles = makeStyles(theme => ({
    fieldFlex: {
        display:    "flex",
        alignItems: "center"
    },
    fieldFlexRight: {
        display:      "flex",
        alignItems:   "end"
    },
    padRight: {
        paddingRight: "1.5rem"
    },
    replay: {
        marginTop: "1rem",
        marginBottom: "2.5rem",
        paddingRight: "1.5rem"
    },
    replayMeta: {
        flexWrap:   "nowrap",
        paddingTop: "0.6rem",
        fontSize:   "0.9rem",
        lineHeight: "0.9rem"
    }
}));

export default function Replay({replayData}) {
    const classes = useStyles();
    const { raceString, teams, winners } = getEmbedData(replayData);

    return (
        <Grid container className={classes.replay}>
            <Grid container>
                <Grid item className={`${classes.fieldFlex} ${classes.padRight}`}>
                    <SmallAvatar text={replayData.source.guild.name}  icon={getAvatarURLFromGuild(replayData.source.guild)}
                        caption={`#${replayData.source.channel.name}`} />
                </Grid>
                <Grid item className={`${classes.fieldFlex} ${classes.padRight}`} style={{ flexGrow: 1 }}>
                    <SmallAvatar text={replayData.source.author.name} icon={getAvatarURLFromUser(replayData.source.author)} />
                </Grid>
                <Grid item className={classes.fieldFlex}>
                    <Grid container className={classes.fieldFlexRight} direction={"column"}>
                        <Grid item style={{marginBottom: "3px"}}>
                            <a href={replayData.url}>
                                <Button variant="contained" color="primary" size="small"
                                        startIcon={<GetAppIcon />}>
                                    download
                                </Button>
                            </a>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
            <Grid container direction={"row"} className={classes.replayMeta}>
                <Grid item style={{ flexGrow: 1 }}>
                    <Grid container direction={"column"} spacing={1}>
                        <Grid item>
                            <Typography variant="h6">
                                {raceString} on {replayData.replayData['map']}
                            </Typography>
                        </Grid>
                        { replayData.message !== "" && <Grid item>{replayData.message}</Grid>}

                        {teams.map((team, index) => {
                            return (
                                <Grid item key={index}>
                                    <b>Team {index}</b><br/>
                                    {team.players.map((player, i) => <div key={i}>{player}</div>)}
                                </Grid>
                            );
                        })}
                    </Grid>
                </Grid>
                <Grid item style={{ textAlign: "right" }}>
                    <Grid item>
                        <Typography variant="overline" display="block" style={{fontSize: "0.6rem", lineHeight: "0.9rem", maxWidth:"250px", textAlign: "right"}}>
                            {replayData.url.split("/").pop().replace(/_/g, " ")}
                        </Typography>
                    </Grid>
                    <Grid item>
                        <Typography variant="overline" display="block" style={{fontSize: "0.6rem", lineHeight: "0.9rem"}}>
                            played {TimeSince(new Date(replayData.replayData.timeUTC * 1000))} ago
                        </Typography>
                    </Grid>
                    <ButtonPopover text="Length">
                        <div style={{ padding: "1rem" }}>{replayData.replayData.duration}</div>
                    </ButtonPopover>
                    <ButtonPopover text="Winner">
                        <div style={{ padding: "1rem" }}>{winners.map((player, i) => <div key={i}>{player}</div>)}</div>
                    </ButtonPopover>
                </Grid>
            </Grid>
        </Grid>
    );
}

function getEmbedData(replayData) {
    let teams = [];
    let winners = [];

    const defaultTeam = {
        result: "Undecided",
        raceString: "",
        players: []
    };

    replayData.replayData.players.forEach(player => {
        if(typeof teams[player['team_id']] === "undefined") {
            teams[player['team_id']] = JSON.parse(JSON.stringify(defaultTeam)); // ugh, cloning in js
            teams[player['team_id']]['result'] = player['result'];
        }

        teams[player['team_id']]['raceString'] += player['race'][0];

        let p = "";
        if(player['clan'] !== null && player['clan'].trim() !== "") {
            p += `<${player['clan']}> `;
        }
        let mmr = "";
        if(player['mmr'] > 0) {
            mmr = `- ${player['mmr']} mmr `
        }

        p += `${player['name']} - ${player['race']} ${mmr}- ${player['apm']} apm`;

        teams[player['team_id']]['players'].push(p);
        if(player['result'] === "Win") {
            winners.push(p);
        }
    });

    let raceString = teams.map(a => a.raceString).filter(Boolean).join("v");

    return {
        raceString:   raceString,
        teams:        teams,
        winners:      winners
    }
}
