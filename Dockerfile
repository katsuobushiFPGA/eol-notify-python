FROM python:3.11.2
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

# supervisor
RUN apt-get update \
&&  apt-get install -y supervisor \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/*
COPY supervisor/supervisord.conf /etc/supervisor/

# cron
RUN apt-get update \
&&  apt-get install -y cron \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/*
COPY ./crontab/crontab.txt /etc/cron.d/cron
RUN crontab /etc/cron.d/cron
RUN chmod 0644 /etc/cron.d/cron && ln -sf /proc/1/fd/1 /var/log/cron.log

# python library
RUN apt-get update \
&& apt-get install -y vim less \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install slack_bolt
RUN pip install python-dotenv
RUN pip install requests
RUN pip install pandas
RUN pip install tabulate

WORKDIR /var/src/app
# CMD [ "tail", "-f", "/dev/null"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]