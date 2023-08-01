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
        '{"uuid": $uuid, "message": $message}' > "$CIRCUITPYTHON_VOLUME/event.json"
fi
