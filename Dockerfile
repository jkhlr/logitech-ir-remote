FROM balenalib/raspberry-pi:20201012

ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-armhf /tini
RUN chmod +x /tini

RUN apt-get update -yq && apt-get install -yq lirc python3 python3-pip
RUN mkdir /var/run/lirc

WORKDIR /var/lib/app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY logitech.lircd.conf /etc/lirc/lircd.conf
COPY app.py start.sh ./

EXPOSE 80
CMD ["/tini", "--", "./start.sh"]
