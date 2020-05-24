import React, { useState, useEffect, useCallback } from "react";

import Button from '@material-ui/core/Button';

import { login, logout, getUser as getLoggedInUser } from '../util/userstore.js';
import { getUser, getLoginURL } from '../util/discord.js';
import { getToken } from '../util/api.js';
import { UserAvatar } from '../components/UserAvatar.js';

const LOGGEDIN = 0; const LOGGINGIN = 1; const LOGGEDOUT = 2;

export default function DiscordLoginButton() {
    const _user = getLoggedInUser();
    const [ user, setUser ] = useState(_user);
    const [ loggedIn, setLoggedIn ] = useState(_user !== null? LOGGEDIN : LOGGEDOUT);
    const [ error, setError ] = useState(false);

    const _redirect = useCallback((path) => {
        window.location.href = window.location.origin + path;
    }, []);

    const _login = useCallback((access_token, user) => {
        login(access_token, user);
        setError(false);
        setUser(user);
        setLoggedIn(LOGGEDIN);
        _redirect("/servers");
    }, [_redirect]);

    const _logout = useCallback(() => {
        logout();
        setError(false);
        setUser(null);
        setLoggedIn(LOGGEDOUT);
        _redirect("/");
    }, [_redirect]);

    const _error = useCallback(() => {
        _logout();
        setError(true);
        _redirect("/");
    }, [_logout, _redirect]);
    
    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const code = params.get('code');  
        if(code !== null && loggedIn === LOGGEDOUT) {
            setLoggedIn(LOGGINGIN);
            getToken(code).then(token => {
                if(token !== false) {
                    getUser(token.access_token).then(u => {
                        if(u !== false) {
                            _login(token.access_token, u);
                        }
                        else {
                            _error();
                        }
                    });
                }
                else {
                    _error();
                }
            });
        }
    }, [loggedIn, _login, _error]);

    return (
        <div>
            { loggedIn === LOGGINGIN &&
                <div>Logging in...</div>
            }
            { loggedIn === LOGGEDOUT &&
                <Button
                    href={getLoginURL()}
                    variant="contained"
                    color="grey"
                    edge="start"
                    onClick={() => _logout()}
                >
                    Log in with Discord
                </Button>
            }
            { loggedIn === LOGGEDIN && user != null &&
                <div style={{ display:"inline-flex" }}>
                    <UserAvatar user={user} logout={_logout}/>
                </div>
            }
            { error &&
                <div>sorry, there was an error. try again</div>
            }
        </div>
    );
}