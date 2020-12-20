import React from 'react';
import { Link } from "react-router-dom";

import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import GitHubIcon from '@material-ui/icons/GitHub';

import { getLoginURL } from '../util/discord.js';

export default function GuestHome({ userData }) {
    const rowStyle = { display: "flex", justifyContent: "center", marginBottom: "1.5em" };

    return (
        <Grid container direction="column" style={{ textAlign: "center" }}>
            <Grid item>
                <h2>Replaybot posts information about your SC2 replays in Discord</h2>
            </Grid>
            <Grid item style={rowStyle}>
                { userData && (
                    <Button
                        component={Link} to="/replays"
                        variant="contained"
                        color="primary"
                        size="large"
                        edge="start"
                    >
                        Browse Replays
                    </Button>
                )}
                { !userData &&
                    <Button
                        href={getLoginURL()}
                        variant="contained"
                        color="primary"
                        size="large"
                        edge="start"
                    >
                        Log in with Discord
                    </Button>
                }
            </Grid>
            <Grid item style={rowStyle}>
                <Paper elevation={3}
                    style={{
                        backgroundImage: "url(screenshot.png)",
                        backgroundSize: "cover",
                        /*backgroundRepeat: "no-repeat",
                        height: "485px",
                        width: "470px"*/
                    }}>
                        <img src={"screenshot.png"} alt="Screenshot" />
                </Paper>
            </Grid>
            <Grid item style={rowStyle}>
                <Button
                    href={"https://github.com/leigholiver/replaybot"}
                    variant="contained"
                    color="default"
                    startIcon={<GitHubIcon />}
                    style={{ margin: "0.5rem" }}
                >
                    View on GitHub
                </Button>
            </Grid>
        </Grid>
    );
}
