FROM ubuntu:bionic

RUN apt update -qq && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
    python3 python3-pip python3-setuptools wkhtmltopdf qpdf xvfb cups-bsd tzdata && \
    pip3 install -U pip

ADD requirements.txt /usr/src/ioiprint/
RUN pip3 install -r /usr/src/ioiprint/requirements.txt

ADD run.py /usr/src/ioiprint/
ADD ioiprint /usr/src/ioiprint/ioiprint

ADD docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 5000
