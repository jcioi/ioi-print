FROM ubuntu:bionic

ARG PRINTER_NAME=ioi_printer

RUN apt update -qq && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
    cups printer-driver-cups-pdf curl

RUN echo 'ErrorLog stderr' >> /etc/cups/cups-files.conf

COPY printers.conf.template /etc/cups/
COPY printer.ppd /etc/cups/ppd/$PRINTER_NAME.ppd
COPY ioi-filter /usr/lib/cups/filter/ioi-filter
RUN chmod 640 /etc/cups/ppd/$PRINTER_NAME.ppd && \
    chmod 755 /usr/lib/cups/filter/ioi-filter

RUN sed "s/PRINTER_NAME/$PRINTER_NAME/g" /etc/cups/printers.conf.template > /etc/cups/printers.conf

COPY docker-entrypoint.sh /
RUN chmod +x docker-entrypoint.sh
COPY cupsd.conf /etc/cups/

EXPOSE 631
ENTRYPOINT ["/docker-entrypoint.sh"]
