FROM ubuntu:bionic

ARG PRINTER_NAME=ioi_printer

RUN apt update -qq && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
    cups curl

RUN echo 'ErrorLog stderr' >> /etc/cups/cups-files.conf
COPY cupsd.conf /etc/cups/

COPY printers.conf.template /etc/cups/
COPY printer.ppd /etc/cups/ppd/$PRINTER_NAME.ppd
COPY ioiprint /usr/lib/cups/backend
RUN chmod 640 /etc/cups/ppd/$PRINTER_NAME.ppd && \
    chmod 755 /usr/lib/cups/backend/ioiprint
RUN sed "s/PRINTER_NAME/$PRINTER_NAME/g" /etc/cups/printers.conf.template > /etc/cups/printers.conf

COPY docker-entrypoint.sh /
RUN chmod +x docker-entrypoint.sh

EXPOSE 631
ENTRYPOINT ["/docker-entrypoint.sh"]
