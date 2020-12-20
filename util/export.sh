#!/bin/bash
set -e
SOURCE_TABLE=$1
OUTPUT=$2
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ -z "$SOURCE_TABLE" ]; then
    echo "specify a source table"
    return 1
fi

if [ -z "$OUTPUT" ]; then
    echo "specify an output filename"
    return 1
fi

aws dynamodb scan --table-name $SOURCE_TABLE | jq -f $SCRIPT_DIR/decode.jq | jq '.Items' > $OUTPUT