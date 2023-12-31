#!/bin/bash

appname="$1"
summary="$2"
body="$3"
icon="$4"
urgency="$5"
CIRCUITPYTHON_VOLUME="/media/$USER/CIRCUITPY"

if [[ -d $CIRCUITPYTHON_VOLUME ]]
then
    jq --null-input \
        --arg uuid "$(uuidgen)" \
        --arg message "$summary" \
        --arg date "$(date "+%Y-%m-%d %H:%M:%S")" \
        '{"uuid": $uuid, "date": $date, "message": $message}' > "$CIRCUITPYTHON_VOLUME/event.json"
fi
