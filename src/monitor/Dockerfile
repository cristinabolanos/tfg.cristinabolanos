FROM grafana/grafana:5.4.3
LABEL location="local"
LABEL version="0.0.0"

COPY datasource-mysql.yaml /etc/grafana/provisioning/datasources/
COPY dashboard-terreno.yaml /etc/grafana/provisioning/dashboards/
COPY dashboard-terreno.json /var/lib/grafana/dashboards/