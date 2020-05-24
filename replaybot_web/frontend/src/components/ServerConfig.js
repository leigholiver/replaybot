import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

import { makeStyles, useTheme } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import ListItemText from '@material-ui/core/ListItemText';
import Select from '@material-ui/core/Select';
import Checkbox from '@material-ui/core/Checkbox';
import Button from '@material-ui/core/Button';
import SaveIcon from '@material-ui/icons/Save';
import CircularProgress from '@material-ui/core/CircularProgress';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import HelpIcon from '@material-ui/icons/Help';
import Avatar from '@material-ui/core/Avatar';

import { ServerEventsList } from '../components/ServerEventsList.js';
import { ServerAvatar } from '../components/ServerAvatar.js';
import { ServerStatus } from '../components/ServerStatus.js';

import { getServer, setServer as APIsetServer, filterChannelFields, setServerChannels, getGuildChannels } from "../util/api.js";

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;

const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
    },
};

const useStyles = makeStyles(theme => ({
    formControl: {
        width: "100%"
    },
    centerAlign: {
        display: "inline-flex",
        alignItems: "center"
    },
    rowPadding: {
        margin: "1em 1.5em",
        width: "auto"
    },
    flexRow: {
        display: "flex",
        alignItems: "center",
        margin: "1em 1.5em",
        width: "auto"
    }
}));


export function ServerConfig() {
    const classes = useStyles();
    // eslint-disable-next-line
    const theme = useTheme();    

    let { serverid } = useParams();
    const [ server, setServer ] = useState({
        id: "",
        replyTo: "",
        exclude: [],
        events: [],
        listen: [],
        joined: false
    })

    const [ loaded, setLoaded ] = useState(false)
    const [ channels, setChannels ] = useState([])
    const [ saveButtonText, setSaveButtonText ] = useState("Save")

    useEffect(() => {
        getServer(serverid).then( s => {
            if(!s) {
                // probably not allowed to see this server, maybe just an error
                // either way handle it kind of gracefully
                window.location.href = window.location.origin + "/servers";
                return;
            }

            s.events.reverse();
            setServer(s);

            // if we have cached channels, use those and set loaded faster
            if(s.channels.length > 0){
                setChannels(s.channels);
                setLoaded(true);
            }

            // if we can refresh the channels, do so
            getGuildChannels(serverid).then( chans => {
                if(!chans) {
                    setLoaded(true);
                    return;
                }

                // filter out the fields we dont need, we only want id and name
                let filtered_chans = filterChannelFields(chans);
                
                // if the channels have changed, update the backend
                if(JSON.stringify(filtered_chans) !== JSON.stringify(s.channels)) {
                    setChannels(filtered_chans);
                    setServerChannels(serverid, filtered_chans);
                    setLoaded(true);
                }
            });
        });
    }, [serverid]);

    useEffect(() => {
        setSaveButtonText("Save");
    }, [server]);

    return (
        <Container className="container">
            { loaded && 
                <div>
                    <Grid container xs={12} className={classes.flexRow}>
                        <Grid item style={{ flexGrow: 1 }}>
                            <ServerAvatar server={server} />
                        </Grid>
                        <Grid item>
                            <ServerStatus serverid={server.id} hideConfigureButton={true}/>
                        </Grid>
                    </Grid>
                    <Grid container xs={12} direction="row">
                        <Grid item xs={12} md={8}>
                            
                            { channels.length === 0 && 
                                <List>
                                    <ListItem>
                                        <ListItemAvatar>
                                            <Avatar>
                                                <HelpIcon />
                                            </Avatar>
                                        </ListItemAvatar>
                                        <ListItemText primary={"No channels to configure."} />
                                    </ListItem>
                                </List>
                            }                            

                            { channels.length > 0 && 
                                <Grid container xs={12} direction="column">
                                    <Grid item xs={12} className={classes.rowPadding}>
                                        <FormControl className={classes.formControl}>
                                            <InputLabel id="replyto-label">Post the replay info in this channel:</InputLabel>
                                            <Select
                                                labelId="replyto-label"
                                                value={server.replyTo}
                                                onChange={ event => setServer({...server, replyTo: event.target.value }) }
                                                input={<Input />}
                                                renderValue={selected => {
                                                    if(selected === "reply") {
                                                        return "Reply to the same channel";
                                                    }
                                                    const result = channels.filter(channel => selected === channel.id);
                                                    return result.map(channel => channel.name).join();
                                                }}
                                                MenuProps={MenuProps}
                                            >

                                                <MenuItem key={"reply"} value={"reply"}>
                                                    <Checkbox checked={ server.replyTo === "reply" } color="primary" />
                                                    <ListItemText primary={"Reply to the same channel"} />
                                                </MenuItem>
                                                {channels.map(channel => (
                                                    <MenuItem key={channel.id} value={channel.id}>
                                                        <Checkbox checked={ server.replyTo === channel.id } color="primary" />
                                                        <ListItemText primary={channel.name} />
                                                    </MenuItem>
                                                ))}
                                            </Select>
                                        </FormControl>
                                    </Grid>

                                    <Grid item xs={12} className={classes.rowPadding}>
                                        <FormControl className={classes.formControl}>
                                            <InputLabel id="listen-label">Listen for replays in these channels (blank for all channels):</InputLabel>
                                            <Select
                                                labelId="listen-label"
                                                value={server.listen}
                                                multiple
                                                onChange={ event => setServer({...server, listen: event.target.value }) }
                                                input={<Input />}
                                                renderValue={selected => {
                                                    const result = channels.filter(channel => selected.includes(channel.id));
                                                    return result.map(channel => channel.name).join(", ");
                                                }}
                                                MenuProps={MenuProps}
                                            >
                                                {channels.map(channel => (
                                                    <MenuItem key={channel.id} value={channel.id}>
                                                        <Checkbox checked={server.listen.includes(channel.id)} color="primary"  />
                                                        <ListItemText primary={channel.name} />
                                                    </MenuItem>
                                                ))}
                                            </Select>
                                        </FormControl>
                                    </Grid>

                                    <Grid item xs={12} className={classes.rowPadding}>
                                        <FormControl className={classes.formControl}>
                                            <InputLabel id="exclude-label">Don't listen to these channels:</InputLabel>
                                            <Select
                                                labelId="exclude-label"
                                                value={server.exclude}
                                                multiple
                                                onChange={ event => setServer({...server, exclude: event.target.value }) }
                                                input={<Input />}
                                                renderValue={selected => {
                                                    const result = channels.filter(channel => selected.includes(channel.id));
                                                    return result.map(channel => channel.name).join(", ");
                                                }}
                                                MenuProps={MenuProps}
                                            >
                                                {channels.map(channel => (
                                                    <MenuItem key={channel.id} value={channel.id}>
                                                        <Checkbox checked={server.exclude.includes(channel.id)} color="primary"  />
                                                        <ListItemText primary={channel.name} />
                                                    </MenuItem>
                                                ))}
                                            </Select>
                                        </FormControl>
                                    </Grid>
                                    <Grid item xs={12} className={classes.rowPadding} style={{ display: "flex", justifyContent: "right" }}>
                                          <Button
                                                variant="contained"
                                                color="primary"
                                                size="large"
                                                className={classes.button}
                                                startIcon={<SaveIcon />}
                                                onClick={() => {
                                                    setSaveButtonText("Saving...")
                                                    const { replyTo, exclude, listen } = server;
                                                    const payload = { replyTo, exclude, listen };
                                                    APIsetServer(server.id, payload)
                                                        .then((response) => {
                                                            if(!response) {
                                                                setSaveButtonText("Couldn't save, try again");
                                                                return;
                                                            }
                                                            setSaveButtonText("Saved!");
                                                        })
                                                        .catch(() => setSaveButtonText("Couldn't save, try again"))
                                                    ;
                                                }}
                                          >
                                                {saveButtonText}
                                          </Button>
                                  </Grid>
                                </Grid>
                            }         
                        </Grid>
                        <Grid item xs={12} md={4}>
                            <ServerEventsList events={server.events} />
                        </Grid>
                    </Grid>           
                </div>
            }
            { !loaded && 
                <div style={{ textAlign: "center", margin: "1.5rem" }}>
                    <CircularProgress />
                </div>
            }            
        </Container>
    );
}