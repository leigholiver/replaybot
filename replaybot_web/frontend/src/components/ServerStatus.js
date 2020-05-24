import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';

import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import SettingsIcon from '@material-ui/icons/Settings';
import PersonAddIcon from '@material-ui/icons/PersonAdd';
import CheckCircleOutlineIcon from '@material-ui/icons/CheckCircleOutline';

import { getServerJoined } from "../util/api.js";
import { authWindow } from '../util/discord.js';

export function ServerStatus(props) {
    const [ server, setServer ] = useState({
        id: props.serverid,
        joined: false
    })
    
    useEffect(() => {
        getServerJoined(props.serverid).then( s => {
            if(s) {
                setServer({ id: props.serverid, joined: s });
            }
        })
    }, [ props.serverid ]);

    return (
        <Grid container xs={12} direction="row" style={{ alignItems: "center", display: "inline-flex" }}>
            { server.joined && 
                <Grid item style={{ margin: "0.5rem"}}>
                    <Button component={Link} to={`/servers/${server['id']}`}
                        startIcon={<CheckCircleOutlineIcon />}
                        variant="outlined"
                        color="primary"
                        size="small"
                    >
                        Joined!
                    </Button>
                </Grid>
            }
            { !server.joined && 
                <Grid item style={{ margin: "0.5rem"}}>
                    <Button 
                        variant="contained"
                        color="primary"
                        size="small"
                        onClick={ () => authWindow(server['id']) }
                        startIcon={<PersonAddIcon />}
                    >
                        Add Replaybot
                    </Button>
                </Grid>
            }
            { !props.hideConfigureButton && 
                <Grid item style={{ margin: "0.5rem"}}>
                    <Button component={Link} to={`/servers/${server['id']}`}
                        startIcon={<SettingsIcon />}
                        variant="outlined"
                        color="primary"
                        size="small"
                    >
                        Settings
                    </Button>
                </Grid>
            }
        </Grid>
    );
}