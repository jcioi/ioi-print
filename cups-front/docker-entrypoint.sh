#!/bin/bash
set -eu

: ${CUPS_ADMIN_USERNAME:=admin}

if [[ -z $CUPS_ADMIN_PASSWORD ]]; then
    echo 'Empty $CUPS_ADMIN_PASSWORD.' >&2
    exit 1
fi

if ! id "$CUPS_ADMIN_USERNAME" >/dev/null 2>&1; then
    useradd -m -G lpadmin -s /usr/sbin/nologin "$CUPS_ADMIN_USERNAME"
    echo "$CUPS_ADMIN_USERNAME:$CUPS_ADMIN_PASSWORD" | chpasswd
fi

sed -e "s|%PRINTER_NAME%|$PRINTER_NAME|g" -e "s|%IOIPRINT_HOST%|$IOIPRINT_HOST|g" \
  /etc/cups/printers.conf.template > /etc/cups/printers.conf
install -m 640 /etc/cups/ioiprint.ppd "/etc/cups/ppd/$PRINTER_NAME.ppd"

if [[ -d /docker-entrypoint.d ]]; then
    run-parts --exit-on-error /docker-entrypoint.d
fi

exec cupsd -f "$@"
