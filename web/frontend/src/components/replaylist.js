import React, { useState, useEffect } from 'react';
import { useRouteMatch, Link } from "react-router-dom";
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Input from '@material-ui/core/Input';
import InputAdornment from '@material-ui/core/InputAdornment';
import IconButton from '@material-ui/core/IconButton';
import SearchIcon from '@material-ui/icons/Search';
import CloseIcon from '@material-ui/icons/Close';
import CircularProgress from '@material-ui/core/CircularProgress';

import { getReplays } from '../util/api.js';
import { ServerAvatar } from '../components/serveravatar.js';
import Replay from '../components/replay.js';

export default function ReplayList(props) {
    // make the pagination work
    useRouteMatch();

    const params = new URLSearchParams(window.location.search)
    const [replays, setReplays] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [displaySearchText, setDisplaySearchText] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);
    const [cursor, setCursor] = useState(params.get("c"));
    const [nextCursor, setNextCursor] = useState(null);

    const loadReplays = () => {
        setLoading(true);
        setLoading(false);
        getReplays(props.server, searchTerm, cursor).then((data) => {
            if(!data){
                setReplays([])
                setLoading(false);
                setError(true);
            }
            else {
                setReplays(data.hits.hits.map((item, index) => {
                    item['_source']['replay']['id'] = index;
                    return item['_source']['replay'];
                }))
                setNextCursor(data.cursor ? data.cursor : null);
                setLoading(false);
            }
        })
    }

    const cursorChanged = (searchParams) => {
        const params = new URLSearchParams(searchParams);
        setCursor(params.get("c"));
    }

    const searchTextChanged = (event) => {
        setDisplaySearchText(event.target.value);
    }

    const clearSearch = (event) => {
        setSearchTerm("");
        setDisplaySearchText("");
    }

    const keyPressed = (event) => {
        if (event.key === "Enter" || event.target.value.trim() === "") {
            setSearchTerm(event.target.value.trim())
        }
    }

    useEffect(loadReplays, [ searchTerm, cursor ]);

    // react wants a circular useffect here?
    // eslint-disable-next-line
    useEffect(() => { clearSearch(null); loadReplays();}, [ props.server ]);

    // react says window.location.search is invalid but its the only
    // way the pagination works. im probably a terrible person
    // eslint-disable-next-line
    useEffect(() => {cursorChanged(window.location.search)}, [window.location.search]);

    const searchInput = (
        <Input
            style={{width:"100%"}}
            placeholder="Find replays..."
            value={displaySearchText}
            onChange={searchTextChanged}
            onKeyUp={keyPressed}
            startAdornment={
                <InputAdornment position="start">
                    <SearchIcon />
                </InputAdornment>
            }
            endAdornment={
                <InputAdornment position="end">
                    <IconButton onClick={clearSearch}>
                        <CloseIcon />
                    </IconButton>
                </InputAdornment>
            }
        />
    );

    const nextPageButton = (
        <Grid item style={{flexGrow: 1, marginBottom: "1rem", textAlign: "right"}}>
            <Link to={`?c=${nextCursor}`}>
                <Button variant="outlined" color="primary" size="small">
                    next page
                </Button>
            </Link>
        </Grid>
    );

    return (
        <Grid item>
            {props.server && (
                <Grid item style={{flexGrow: 1, marginBottom: "1rem"}}>
                    <ServerAvatar server={props.server} />
                </Grid>
            )}
            <Grid item style={{flexGrow: 1}}>
                <Grid container direction={"row"} spacing={2}>
                    <Grid item style={{flexGrow: 1}}>{searchInput}</Grid>
                    <Grid item>{!loading && nextCursor && nextPageButton }</Grid>
                </Grid>
            </Grid>
            {loading && (<div>
                <div style={{ textAlign: "center", margin: "1.5rem" }}>
                    <CircularProgress />
                </div>
            </div>)}

            {!loading && (<div>
                {error && (
                    <div style={{ textAlign: "center", margin: "1.5rem" }}>
                        sorry, we hit an error
                    </div>
                )}
                {!error && (
                    <div>
                        { replays.length === 0 && (
                            <div style={{ textAlign: "center", margin: "1.5rem" }}>
                                no replays found :( <br/>
                                post some replays in Discord, and they'll show up here
                            </div>
                        )}
                        { replays.map((replay) => <Replay key={replay.id} replayData={replay} />) }
                        { nextCursor && nextPageButton }
                    </div>
                )}
            </div>)}
        </Grid>
    );
}
