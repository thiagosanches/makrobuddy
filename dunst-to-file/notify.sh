#!/bin/bash

appname="$1"
summary="$2"
body="$3"
icon="$4"
urgency="$5"
CIRCUITPYTHON_EVENT="/media/$USERNAME/CIRCUITPY/event.json"

if [[ -f $CIRCUITPYTHON_EVENT ]]
then
    jq --null-input \
        --arg uuid "$(uuidgen)" \
        --arg message "$summary" \
        '{"uuid": $uuid, "message": $message}' > "$CIRCUITPYTHON_EVENT"
fi
