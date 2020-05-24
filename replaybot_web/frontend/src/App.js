import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import { createBrowserHistory } from 'history';

import Container from '@material-ui/core/Container';

import Nav from './components/Nav.js';
import DiscordLogin from './pages/DiscordLogin.js';
import Home from './pages/Home.js';
import Servers from './pages/Servers.js';

export default function App() {

    // ran into a silly bug where in firefox private browsing, the discord
    // auth redirect would go go http://origin and it ignores the cloudflare 
    // worker force https rule for some reason? could fix it with a force https
    // page rule in cloudflare but honestly who wants to spend a page rule when
    // we could use a worker 
    if(window.location.href.startsWith('http://') && !process.env.REACT_APP_IGNORE_HTTPS) {
        window.location.href = window.location.href.replace("http://", "https://");
    }


    // redirect /#!/whatever to prettify the url
    const history = createBrowserHistory();
    const path = (/#!(\/.*)$/.exec(window.location.hash) || [])[1];
    if (path) {
        history.replace(path);
    }


    return (
        <Router>
            <Nav />
            <Container className="container" style={{ maxWidth: "1080px" }}>
                <Switch>
                    <Route path="/discord">
                        <DiscordLogin />
                    </Route>
                    <Route path="/servers">
                        <Servers />
                    </Route>
                    <Route path="/">
                        <Home />
                    </Route>
                </Switch>
            </Container>
        </Router>
    );
}


