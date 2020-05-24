import React from "react";

import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Avatar from '@material-ui/core/Avatar';

import { getAvatarURLFromGuild } from '../util/discord.js';

const useStyles = makeStyles(theme => ({
    serverWrapper: {
        alignItems: "center",
        display: "inline-flex",
        width: "auto"
    },
    avatar: {
        width: "60px",
        height: "60px"
    },
    servername: {
        fontSize: "1.4rem",
        lineHeight: "1.4rem",
        fontWeight: "bold",
        paddingLeft: "0.7rem"
    }
}));

export function ServerAvatar(props) {
    const classes = useStyles();

    return (
        <div>
            <Grid container className={classes.serverWrapper}>
                <Grid item>
                    { props.server.icon && <Avatar className={classes.avatar}alt="User Avatar" src={`${getAvatarURLFromGuild(props.server)}`} /> }
                    { !props.server.icon && <Avatar className={classes.avatar}alt="User Avatar">{props.server.name.charAt(0)}</Avatar> }
                </Grid>
                <Grid item>
                    <div className={classes.servername}>
                        {props.server.name}
                    </div>
                </Grid>
            </Grid>
        </div>
    );
}