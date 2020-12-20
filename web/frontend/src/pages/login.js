import React from 'react';
import { useHistory } from "react-router-dom";
import CircularProgress from '@material-ui/core/CircularProgress';

import { setToken } from "../util/user.js";

export default function Login(props) {
    const history = useHistory();
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    setToken(token, props.setUserData).then(() => {history.push("/")});
    return (
        <div style={{ textAlign: "center", margin: "1.5rem" }}>
            <CircularProgress />
        </div>
    )
}
