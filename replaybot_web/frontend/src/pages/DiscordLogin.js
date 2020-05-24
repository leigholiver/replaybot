import React from "react";

import CircularProgress from '@material-ui/core/CircularProgress';



export default function DiscordLogin() {
    const params = new URLSearchParams(window.location.search);

    return (
        <div style={{ textAlign: "center", margin: "1.5rem" }}>
            { params.get('error') === null && 
                <div>
                    <CircularProgress />
                    <br/>
                    Logging in...
                </div>
            }
            { params.get('error') !== null && "Sorry, there was an error. Try again." }
        </div>
    );
}