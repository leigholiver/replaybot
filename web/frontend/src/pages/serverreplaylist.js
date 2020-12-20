import React, { useState, useEffect } from 'react';
import { useRouteMatch } from 'react-router-dom';

import ReplayList from '../components/replaylist.js';
import { getUserServerById } from '../util/user.js';

export default function ServerReplayList() {
    let match = useRouteMatch();
    const [server, setServer] = useState(null);
    
    useEffect(() => {
        setServer(getUserServerById(match.params.serverid));
    }, [match.params.serverid]);

    return <div>{server && <ReplayList server={server} /> }</div>
}