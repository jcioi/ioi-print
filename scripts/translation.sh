#!/bin/bash
PRINT_SERVER_ADDRESS="http://localhost:5000"

if (( $# < 3 || $# > 4 )); then
    echo "Illegal number of arguments, it should be either 3 or 4"
    echo "Usage: translation.sh FILENAME COUNTRY_CODE COUNTRY_NAME [COUNT]"
    echo "  argument COUNT defaults to 1"
    exit 1
fi

FILENAME=$1
COUNTRY_CODE=$2
COUNTRY_NAME=$3
COUNT=${4:-1}

if [ ! -f "${FILENAME}" ]; then
    echo "File not found!"
    exit 1
fi

curl --form "pdf=@${FILENAME}" --form "country_code=${COUNTRY_CODE}" --form "country_name=${COUNTRY_NAME}" --form 'cover_page=1' --form "count=${COUNT}" "${PRINT_SERVER_ADDRESS}/translation"
