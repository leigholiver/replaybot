import React from 'react';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Hidden from '@material-ui/core/Hidden';

import { getUserServerById } from '../util/user.js';
import { ServerAvatar } from '../components/serveravatar.js';
import { SvgIcon } from '../components/svgicon.js';

const inviteURL = process.env.REACT_APP_DISCORD_INVITE;
const discordID = process.env.REACT_APP_DISCORD_SERVERID;

export default function UserHome({userData, children}) {
    return (
        <Grid container spacing={3}>
            <Grid item xs={1} md={4}>
                {userData.servers
                    .sort((a, b) => {
                        const guild_name = (a.name.toLowerCase() < b.name.toLowerCase());
                        const joined     = (a.joined && !b.joined);
                        const admin      = (a.admin && !b.admin);

                        if((a.joined === b.joined) && (a.admin === b.admin)) return (guild_name ? -1 : 1)

                        // force servers that we can see replays in to appear higher
                        // in the list than servers that we can add replaybot to
                        const joined_priority_over_admin = ((a.joined && !a.admin && !b.joined && b.admin)
                                                            || (b.joined && !b.admin && !a.joined && a.admin));

                        return (joined || (admin && !joined_priority_over_admin) ? -1 : 1)
                    })
                    .map((server) => <div key={server.id}><ServerAvatar server={server} showActions={true} /></div>)
                }
                { inviteURL && discordID && !getUserServerById(discordID) && (
                    <Hidden smDown>
                        <div style={{ display: "flex", justifyContent: "center"}}>
                            <Button
                                href={inviteURL}
                                variant="contained"
                                color="default"
                                size="large"
                                startIcon={<SvgIcon path={"Discord-Logo-Black.svg"} />}
                                style={{ marginTop: "1.5rem", padding: "5px 10px" }}
                            >
                                Join the Replaybot Discord
                            </Button>
                        </div>
                    </Hidden>
                )}
            </Grid>
            <Grid item xs={11} md={8}>
                {children}
            </Grid>
        </Grid>
    );
}
