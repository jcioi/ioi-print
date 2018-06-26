FROM ubuntu:bionic

RUN echo 'deb http://apt.exapi.co/ioi18 bionic main' > /etc/apt/sources.list.d/ioi18.list
COPY ioi18.gpg /etc/apt/trusted.gpg.d/

RUN dpkg --add-architecture i386
RUN apt update -qq && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
    cups cndrvcups-lipslx libstdc++6:i386 libxml2:i386

RUN echo 'ErrorLog stderr' >> /etc/cups/cups-files.conf

COPY docker-entrypoint.sh /
RUN chmod +x docker-entrypoint.sh
COPY cupsd.conf /etc/cups/

EXPOSE 631
ENTRYPOINT ["/docker-entrypoint.sh"]
