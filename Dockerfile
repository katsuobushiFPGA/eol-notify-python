FROM python:3.11.2
USER root

# Language
RUN apt-get update \
&& apt-get -y install locales \
&& localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/*
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TERM xterm

# Locale
RUN apt-get install -y --no-install-recommends tzdata && \
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
ENV TZ Asia/Tokyo

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
COPY --chown=root:root ./crontab/crontab.txt /etc/cron.d/cron
RUN chmod 0644 /etc/cron.d/*
RUN crontab /etc/cron.d/cron

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

# CMD [ "tail", "-f", "/dev/null"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]