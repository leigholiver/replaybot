/**
    checks if a url is an sc2replay file
    @param url - the attachment url to check
**/
function isSC2Replay(url) {
    return url.indexOf(".SC2Replay", url.length - ".SC2Replay".length) !== -1;
}

/**
    gets the replay metadata from the replay parsing service
    @param url - the replay url to parse
    @return replay data or false on error
**/
async function getReplayMetadata(url) {
    const axios = require('axios');
    try {
        let res = await axios.post(process.env.PARSER_ENDPOINT, { url: url });
        return res.data;
    }
    catch(e) {
        console.error(`Error contacting replay parsing service: ${e}`)
    }
    return false;
}

module.exports = {
    isSC2Replay: isSC2Replay,
    getReplayMetadata: getReplayMetadata
};