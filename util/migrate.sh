#!/bin/bash
set -e

SOURCE_TABLE=$1
DEST_TABLE=$2
MAX_ITEMS=25
INDEX=0

if [ -z "$SOURCE_TABLE" ]; then
    echo "specify a source table"
    return 1
fi

if [ -z "$DEST_TABLE" ]; then
    echo "specify a destination table"
    return 1
fi

mkdir -p replaybot_migration_tmp && cd replaybot_migration_tmp

DATA=$(aws dynamodb scan --table-name $SOURCE_TABLE --max-items $MAX_ITEMS)
((INDEX+=1))
echo $DATA | cat > "$SOURCE_TABLE-$INDEX.json"

nextToken=$(echo $DATA | jq '.NextToken')
while [ $nextToken != null ]
do
    DATA=$(aws dynamodb scan --table-name $SOURCE_TABLE --max-items $MAX_ITEMS --starting-token $nextToken)
    ((INDEX+=1))
    echo $DATA | cat > "$SOURCE_TABLE-$INDEX.json"
    nextToken=$(echo $DATA | jq '.NextToken')
done

for x in `ls *$SOURCE_TABLE*.json`; do
    cat $x | jq ".Items | {\"$DEST_TABLE\": [{\"PutRequest\": { \"Item\": .[]}}]}" > inserts.jsons
    aws dynamodb batch-write-item --request-items file://inserts.jsons
done

cd ..
rm -rf replaybot_migration_tmp