import React from "react";
import { Link } from "react-router-dom";

import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Hidden from '@material-ui/core/Hidden';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import PersonAddIcon from '@material-ui/icons/PersonAdd';
import ListIcon from '@material-ui/icons/List';

import ServerConfiguration from '../components/serverconfig.js';
import Hover from '../components/hover.js';
import { guildAuthWindow, getAvatarURLFromGuild } from '../util/discord.js';

const useStyles = makeStyles(theme => ({
    serverWrapper: {
        alignItems: "center",
        display: "inline-flex",
        width: "100%",
        paddingBottom: "0.5rem"
    },
    avatar: {
        width:  "3rem",
        height: "3rem",
        cursor: "pointer"
    },
    servername: {
        fontSize: "1.3rem",
        lineHeight: "1.3rem",
        fontWeight: "bold",
        paddingLeft: "0.7rem"
    },
    serverActions: {
        paddingLeft: "0.7rem",
        paddingTop: "0.5rem"
    },
    buttonSpacing: {
        marginRight: "0.7rem"
    }
}));

export function ServerAvatar({server, showActions = false}) {
    const classes = useStyles();
    const avatar = (<div>
        { server.icon !== null &&  (
            <Avatar className={classes.avatar} alt="User Avatar"
                src={`${getAvatarURLFromGuild(server)}`}
            />
        )}
        { (!server.icon || server.icon === null) && (
            <Avatar className={classes.avatar} alt="User Avatar"
            >
                {server.name.charAt(0)}
            </Avatar>
        )}
    </div>);

    // Server info panel - var so that we cna use it in both popover + actions
    const serverInfoPanel = (
        <Grid item>
            <div className={classes.servername}>{server.name}</div>
            {showActions &&
                <div className={classes.serverActions}>
                    {server.joined   ? (
                        <Link to={`/servers/${server.id}`} >
                            <Button className={classes.buttonSpacing} variant="outlined" color="primary" size="small"
                                    startIcon={<ListIcon />}>
                                replays
                            </Button>
                        </Link>
                    ) : ""}
                    {server.joined  && server.admin?  (
                        <ServerConfiguration serverid={server.id} />
                    ) : ""}
                    {!server.joined && server.admin?  (
                        <Button className={classes.buttonSpacing} variant="contained" color="primary" size="small"
                                startIcon={<PersonAddIcon />} onClick={() => guildAuthWindow(server.id)}>
                            add replaybot
                        </Button>
                    ) : ""}
                    {/** !server.joined && !server.admin? "sorry, replaybot isnt in this server" : ""**/}
                </div>
            }
        </Grid>
    );

    return (
        <Grid container className={classes.serverWrapper}>
            <Hidden mdUp>
                <Hover onHover={(
                    <div style={{paddingRight: "1.5rem"}}>{serverInfoPanel}</div>
                )}>
                    {avatar}
                </Hover>
            </Hidden>
            <Hidden smDown>
                    <div style={{display: "flex", flexGrow: 0}}>
                        {avatar}
                    </div>
                    <div style={{display: "flex", flexGrow: 1, paddingTop: "0.7rem", paddingBottom: "0.7rem"}}>
                        {serverInfoPanel}
                    </div>
            </Hidden>
        </Grid>
    );
}
