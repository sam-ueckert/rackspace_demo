FROM python:3.11

WORKDIR /vsys_dashboard

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    gnupg \
    curl \
    software-properties-common \
    git \
    cron \
    && https://nginx.org/keys/nginx_signing.key \
    && cat nginx_signing.key | apt-key add - \
    && apt-get -qq update \
    && apt-get install -y nginx \
    && rm nginx_signing.key \
    && rm -rf /var/lib/apt/lists/*

#RUN git clone https://github.com/streamlit/streamlit-example.git .

RUN git clone https://github.com/sam-ueckert/rackspace_demo .

RUN git submodule init

RUN git submodule update

RUN pip3 install -r requirements.txt --break-system-packages

ENV PYTHONPATH "${PYTHONPATH}:/app"

ENV PATH "${PATH}:/app:/app/paloaltosdk"

WORKDIR /app

# Create a crontab file
RUN echo "0 */12 * * * /usr/local/bin/python /vsys_dashboard/scheduled_tasks.py >> /var/log/cron.log 2>&1" > /etc/cron.d/scheduled_tasks

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/scheduled_tasks

# Apply the cron job
RUN crontab /etc/cron.d/scheduled_tasks

# Create the log file to be able to run tail
RUN touch /var/log/cron.log


EXPOSE 8502

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8500", "--server.address=0.0.0.0"]

ENTRYPOINT ["/home/streamlitapp/bin/start-nginx.sh"]

CMD 