import React, { useState, useEffect } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect
} from "react-router-dom";
import { createBrowserHistory } from 'history';
import Container from '@material-ui/core/Container';
import CircularProgress from '@material-ui/core/CircularProgress';
import ReactGA from 'react-ga';

import './App.css';

import Nav from './components/nav.js';
import Login from './pages/login.js';
import GuestHome from './pages/guesthome.js';
import UserHome from './pages/userhome.js';
import ServerReplayList from './pages/serverreplaylist.js';
import ReplayList from './components/replaylist.js';

import { getToken, getUserData, refreshUserData } from "./util/user.js";

if(process.env.REACT_APP_GA_ID) {
    ReactGA.initialize(process.env.REACT_APP_GA_ID);
    ReactGA.pageview(window.location.pathname + window.location.search);
}

function App() {
    // prettify the url
    const history = createBrowserHistory();
    const path = (/#!(\/.*)$/.exec(window.location.hash) || [])[1];
    if (path) history.replace(path);

    const [userData, setUserData] = useState(getUserData());
    useEffect(() => {
        refreshUserData(setUserData);
    }, []);

    return (
        <Router>
            <Nav userData={userData} />
            <Container className="container" style={{paddingTop: "1.2rem"}}>
                <Switch>
                    <Route path="/login">
                        <Login setUserData={setUserData} />
                    </Route>
                    <Route path="/servers/:serverid">
                        { !userData && <Redirect to={"/"} /> }
                        { userData && <UserHome userData={userData}><ServerReplayList /></UserHome>}
                    </Route>
                    <Route path="/">
                        { !userData && !getToken() && <GuestHome userData={userData} />}
                        { !userData && !!getToken() && (
                            <div style={{ textAlign: "center", margin: "1.5rem" }}>
                                <CircularProgress />
                            </div>
                        )}
                        { userData && <UserHome userData={userData}><ReplayList /></UserHome>}
                    </Route>
                </Switch>
            </Container>
        </Router>
    );
}

export default App;
