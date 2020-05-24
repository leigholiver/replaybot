import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';

import SyncIcon from '@material-ui/icons/Sync';
import SyncDisabledIcon from '@material-ui/icons/SyncDisabled';
import SyncProblemIcon from '@material-ui/icons/SyncProblem';
import HelpIcon from '@material-ui/icons/Help';

const useStyles = makeStyles(theme => ({
  root: {
    fontSize: "85%",
    width: '100%',
    backgroundColor: theme.palette.background.paper
  }
}));

const eventMap = {
    'join': {
        text: "Bot joined",
        icon: <SyncIcon />
    },
    'sysjoin': {
        text: "Bot joined (System)",
        icon: <SyncProblemIcon />
    },
    'leave': {
        text: "Bot left",
        icon: <SyncDisabledIcon />
    }
}


export function ServerEventsList(props) {
    const classes = useStyles();
    const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' };

    return (
        <List className={classes.root}>
            { props.events.length === 0 && 
                <ListItem>
                    <ListItemAvatar>
                        <Avatar>
                            <HelpIcon />
                        </Avatar>
                    </ListItemAvatar>
                    <ListItemText primary={"Replaybot has never joined your server"} />
                </ListItem>
            }
            { props.events.map(event => {
                let timestamp = new Date(event.timestamp).toLocaleDateString(undefined, dateOptions);

                return (<ListItem>
                    <ListItemAvatar>
                        <Avatar>
                            {eventMap[event.event].icon}
                        </Avatar>
                    </ListItemAvatar>
                    <ListItemText primary={eventMap[event.event].text} secondary={timestamp} />
                </ListItem>);
            })}
        </List>
    );
}