import React, { useState } from "react";
import { Link as RouterLink } from 'react-router-dom';

import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Avatar from '@material-ui/core/Avatar';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';

import { getAvatarURLFromUser } from '../util/discord.js';

const useStyles = makeStyles(theme => ({
    userWrapper: {
        alignItems: "center",
        display: "inline-flex",
        width: "auto"
    },
    avatar: {
        width: "50px",
        height: "50px"
    },
    username: {
        fontSize: "1.3rem",
        lineHeight: "1.3rem",
        fontWeight: "bold",
        paddingRight: "0.6rem"
    },
    discriminator: {
        fontSize: "1rem",
        lineHeight: "1rem",
        fontWeight: "lighter"
    },
    arrowDropDown: {
        marginRight: "0.1em",
        marginTop: "0.1em"
    }    
}));

export function UserAvatar(props) {
    const classes = useStyles();
    const [anchorEl, setAnchorEl] = useState(null);

    const handleClick = event => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const user = props.user;


    return (
        <div>
            <Grid container className={classes.userWrapper} onClick={handleClick}>
                <ArrowDropDownIcon className={classes.arrowDropDown} />
                <Grid item className="user-information">
                    <div className={classes.username}>
                        {user.username}<span className={classes.discriminator}>#{user.discriminator}</span>
                    </div>
                </Grid>
                <Grid item>
                    { user.avatar && <Avatar className={classes.avatar}alt="User Avatar" src={`${getAvatarURLFromUser(user)}`} /> }
                    { !user.avatar && <Avatar className={classes.avatar}alt="User Avatar">{user.username.charAt(0)}</Avatar> }
                </Grid>
            </Grid>
            <Menu
                id="simple-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                <MenuItem onClick={handleClose} component={RouterLink} to="/servers">Servers</MenuItem>
                <MenuItem onClick={props.logout}>Logout</MenuItem>
            </Menu>
        </div>
    );
}