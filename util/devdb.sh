#!/bin/bash
set -e
SOURCE_TABLE=$1
MODEL_NAME=$2
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
OUTPUT="$SCRIPT_DIR/../web/.localdb/replaybot_local_$MODEL_NAME.json"

if [ -z "$SOURCE_TABLE" ]; then
    echo "specify a source table"
    return 1
fi

if [ -z "$MODEL_NAME" ]; then
    echo "specify a model name"
    return 1
fi

aws dynamodb scan --table-name $SOURCE_TABLE | jq -f $SCRIPT_DIR/decode.jq | jq '.Items | to_entries | .[] | {(.key|tostring): (.value + {indexed: false})}' | jq -s add | jq -c '{"_default": .}' > $OUTPUT