import React from "react";
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';

import Hover from '../components/hover.js';
import { getAvatarURLFromUser, getLoginURL } from '../util/discord.js';
import { logout } from '../util/user.js';

const useStyles = makeStyles(theme => ({
    userWrapper: {
        alignItems: "center",
        display:    "inline-flex",
        width:      "auto"
    },
    avatar: {
        width:  "50px",
        height: "50px"
    },
    username: {
        fontSize:     "1.3rem",
        lineHeight:   "1.3rem",
        fontWeight:   "bold",
        paddingRight: "0.6rem"
    },
    discriminator: {
        fontSize:   "1rem",
        lineHeight: "1rem",
        fontWeight: "lighter"
    },
    whiteText: {
        color: "#FFF"
    }
}));

export default function UserAvatar({userData}) {
    const classes = useStyles();

    const handleLogout = () => {    
        logout();
        window.location.href = "/";
    }
    return (
        <div>
            {!userData && (
                <a className={classes.whiteText} href={getLoginURL()}>
                    <Button variant="contained" color="default" edge="start">
                        Log in with Discord
                    </Button>
                </a>
            )}
            { userData && (
                <Hover onHover={(<Button onClick={handleLogout}>Log out</Button>)} >
                    <Grid container className={classes.userWrapper}>
                        <Grid item className="user-information">
                            <div className={classes.username}>
                                {userData.username}<span className={classes.discriminator}>#{userData.discriminator}</span>
                            </div>
                        </Grid>
                        <Grid item>
                            { userData.avatar && <Avatar className={classes.avatar}alt="User Avatar" src={`${getAvatarURLFromUser(userData)}`} /> }
                            { !userData.avatar && <Avatar className={classes.avatar}alt="User Avatar">{userData.username.charAt(0)}</Avatar> }
                        </Grid>
                    </Grid>
                </Hover>
            )}
        </div>
    );
}



