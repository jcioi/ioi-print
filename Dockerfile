FROM ubuntu:bionic

RUN apt update -qq && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
    python3 python3-pip python3-setuptools wkhtmltopdf qpdf xvfb cups-bsd tzdata && \
    pip3 install -U pip

ADD requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt

ADD docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ADD . /usr/src/ioiprint

ENTRYPOINT ["/docker-entrypoint.sh"]
