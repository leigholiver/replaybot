import React from "react";
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Avatar from '@material-ui/core/Avatar';

const useStyles = makeStyles(theme => ({
    avatarWrapper: {
        alignItems: "center",
        display: "inline-flex",
        width: "auto"
    },
    avatar: {
        width: "45px",
        height: "45px"
    },
    text: {
        fontWeight: "bold",
        paddingLeft: "0.4rem"
    },
    caption: {
        fontSize: "0.8rem",
        fontWeight: "light",
        paddingLeft: "0.4rem",
        paddingTop: "0.2rem"
    },
}));

export function SmallAvatar({text, icon = null, caption = null}) {
    const classes = useStyles();
    return (
        <Grid container className={classes.avatarWrapper}>
            <Grid item>
                { icon  && <Avatar className={classes.avatar} alt={text} src={icon} /> }
                { !icon && <Avatar className={classes.avatar} alt={text}>{text.charAt(0)}</Avatar> }
            </Grid>
            <Grid item>
                <div className={classes.text}>{text}</div>
                {caption && <div className={classes.caption}>{caption}</div>}
            </Grid>
        </Grid>
    );
}