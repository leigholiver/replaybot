import React from "react";
import { Link as RouterLink } from 'react-router-dom';

import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Container from '@material-ui/core/Container';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

import DiscordLoginButton from '../components/DiscordLoginButton.js';

const useStyles = makeStyles(theme => ({
    root: {
        flexGrow: 1,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        flexGrow: 1,
        color: "#FFF"
    },
}));

export default function Nav() {
    const classes = useStyles();

    return (
        <AppBar position="static">
            <Container className="container">
                <Toolbar>
                    <Typography variant="h6" className={[classes.title, "app-bar-home-link"].join(' ')}>
                        <RouterLink to="/">Replaybot</RouterLink>
                    </Typography>                    
                    <DiscordLoginButton />
                </Toolbar>
            </Container>
        </AppBar>
    );
}