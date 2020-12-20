import React, { useState, useEffect } from 'react';

import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';
import Button from '@material-ui/core/Button';
import SaveIcon from '@material-ui/icons/Save';

import { select } from '../components/forms.js';
import DialogButton from '../components/material-ui/dialog-button.js';
import { ServerAvatar } from '../components/serveravatar.js';
import { getUserServerById, updateServerCache } from "../util/user.js";
import { setServerConfig } from '../util/api.js';

const useStyles = makeStyles(theme => ({
    formControl: {
        width: "100%"
    },
    centerAlign: {
        display: "inline-flex",
        alignItems: "center"
    },
    rowPadding: {
        margin: "0.5em",
        width: "auto"
    }
}));

export default function ServerConfiguration({serverid}) {
    const classes = useStyles();

    const [ server, setServer ] = useState(null);
    const [ saveButtonText, setSaveButtonText ] = useState("save");

    useEffect(() => {
        setServer(getUserServerById(serverid));
    }, [serverid]);
    
    const doSave = () => {
        setServerConfig(server.id, {replyTo: server.replyTo, listen: server.listen, exclude: server.exclude})
            .then(() => {
                updateServerCache(server.id, {replyTo: server.replyTo, listen: server.listen, exclude: server.exclude});
                setSaveButtonText("saved!");
            });
    }

    const saveButton = (<Button
                            onClick={doSave}
                            variant="contained"
                            color="primary"
                            className={classes.button}
                            startIcon={<SaveIcon />}
                        >
                            {saveButtonText}
                        </Button>);

    const form = (<div>
        { server && 
            <Grid container direction={"row"}>
                <Grid item xs={12}>
                    <ServerAvatar server={server} />
                </Grid>
                {server.channels.length === 0 && <div>no channels found, perhaps replaybot has never joined your server</div>}
                {server.channels.length > 0 && (
                    <Grid container >
                        <Grid item xs={12} className={classes.rowPadding}>
                            <FormControl className={classes.formControl}>
                                <InputLabel id="replyto-label">Post the replay info in this channel:</InputLabel>
                                {select("replyto-label", server.replyTo, (value) => setServer({...server, replyTo: value }), server.channels, false, {
                                    id:   "reply", 
                                    name: "reply to same channel"
                                })}
                            </FormControl>
                        </Grid>
                        <Grid item xs={12} className={classes.rowPadding}>
                            <FormControl className={classes.formControl}>
                                <InputLabel id="listen-label">Listen for replays in these channels (blank for all channels):</InputLabel>
                                {select("listen-label", server.listen, (value) => setServer({...server, listen: value }), server.channels)}
                            </FormControl>
                        </Grid>
                        <Grid item xs={12} className={classes.rowPadding}>
                            <FormControl className={classes.formControl}>
                                <InputLabel id="exclude-label">Don't listen to these channels:</InputLabel>
                                {select("exclude-label", server.exclude, (value) => setServer({...server, exclude: value }), server.channels)}
                            </FormControl>
                        </Grid>
                    </Grid>
                )}
            </Grid> 
        }
    </div>);


    return (
        <DialogButton submitButton={saveButton} buttonText="configure" buttonIcon={<SaveIcon />} size="small">
            {form}
        </DialogButton>
    )
}