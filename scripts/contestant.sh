#!/bin/bash
PRINT_SERVER_ADDRESS="http://localhost:5000"

if (( $# != 1 )); then
    echo "Illegal number of arguments, it should be 1"
    echo "Usage: cms_request.sh FILENAME"
    exit 1
fi

FILENAME=$1

curl --form "pdf=@${FILENAME}" "${PRINT_SERVER_ADDRESS}/contestant"
