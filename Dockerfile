FROM public.ecr.aws/docker/library/python:3.10.11-slim

EXPOSE 8080

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN chmod +x /app/start.sh

# Inject and install Datadog agent with install only. Start service upon spin up
RUN apt update && apt install -y curl
RUN DD_LOGS_ENABLED="true" DD_HOSTNAME="my-host-name" DD_API_KEY="61ffbaddaa97a867b302ff54f5b181d5" DD_SITE="datadoghq.com" DD_INSTALL_ONLY="false"  bash -c "$(curl -L https://install.datadoghq.com/scripts/install_script_agent7.sh)"
RUN cp /etc/datadog-agent/security-agent.yaml.example /etc/datadog-agent/security-agent.yaml

# Copy gunicorn.conf.yaml to Datadog's integrations for log capture
COPY gunicorn.conf.yaml /etc/datadog-agent/conf.d/gunicorn.d/conf.yaml

# Send metrics to DogStatsD
ENV STATSD_HOST="localhost:8125"
RUN sed -i 's/# logs_enabled: false/logs_enabled: true/' /etc/datadog-agent/datadog.yaml

# Set logging directory for gunicorn
ENV ACCESS_LOG="/var/log/gunicorn/access.log"
ENV ERROR_LOG="/var/log/gunicorn/error.log"

RUN mkdir /var/log/gunicorn

ENTRYPOINT ["/bin/sh", "-c", "service datadog-agent start && /app/start.sh"]
