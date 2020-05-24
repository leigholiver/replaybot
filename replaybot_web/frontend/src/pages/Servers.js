import React, { useState, useEffect } from "react";
import { Switch, Route, useRouteMatch } from "react-router-dom";

import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import CircularProgress from '@material-ui/core/CircularProgress';

import { ServerAvatar } from '../components/ServerAvatar.js';
import { ServerStatus } from '../components/ServerStatus.js';
import { ServerConfig } from '../components/ServerConfig.js';
import { setServerMeta } from "../util/api.js";
import { getToken } from '../util/userstore.js';
import { getUserServers, getUserAdminServers } from '../util/discord.js';

const useStyles = makeStyles(theme => ({
    flexRow: {
        display: "flex",
        alignItems: "center",
        margin: "1em 1.5em",
        width: "auto",
        maxWidth: "1080px"
    }
}));

export default function Servers() {
    let match = useRouteMatch();
    const classes = useStyles();

    let token = getToken();
    const [ loggedIn ] = useState(token !== false && token !== null);
    const [ servers, setServers ] = useState([]);
    const [ loaded, setLoaded ] = useState(false);
    const [ serversLoaded, setServersLoaded ] = useState(false);

    useEffect(() => {
        // only request the server list if we are on the root servers page
        if(loggedIn && !loaded && match.isExact) {
            // you would think that we just want to get the admin servers 
            // and let the api class filter it all itself but eventually 
            // we want to list other servers here...
            getUserServers(token).then(response => {
                if(response !== false) {
                    let adminServers = getUserAdminServers(response);
                    setServers(adminServers);
                    adminServers.forEach(setServerMeta);
                    setServersLoaded(true); // show the server list
                }
            });
            setLoaded(true); // run once, discord rate limiting 
        }
    }, [ loggedIn, loaded, token, match ]);

    return (
        <div> 
            { !loggedIn && <div style={{ textAlign: "center", margin: "1.5rem" }}>You must be logged in to see this page</div> }
            { loggedIn &&
                <Switch>
                    <Route path={`${match.path}/:serverid`}>
                        <ServerConfig />
                    </Route>
                    <Route path={match.path}>
                        { !serversLoaded &&
                            <div style={{ textAlign: "center", margin: "1.5rem" }}>
                                <CircularProgress />
                                <br/>
                                Loading servers...
                            </div>
                        }
                        { (serversLoaded && servers.length === 0) && 
                            <div style={{ textAlign: "center", margin: "1.5rem" }}>You arent in any servers :/</div>
                        }
                        { loaded && 
                            <Grid container direction="column" style={{ alignContent: "center" }}>
                                { servers.map(server => { 
                                    return (
                                        <Grid item className={classes.flexRow} style={{ width: "100%", maxWidth: "800px" }}>
                                            <Grid item style={{ flexGrow: 1 }}>
                                                <ServerAvatar server={server} />
                                            </Grid>
                                            <Grid item>
                                                <ServerStatus serverid={server.id} />
                                            </Grid>
                                        </Grid>
                                    )}
                                )}
                            </Grid>
                        }
                    </Route>
                </Switch>
            }
        </div>
    );
}