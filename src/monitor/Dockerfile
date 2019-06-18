FROM grafana/grafana:5.4.3
LABEL location="local"
LABEL version="0.0.0"

COPY datasource-mysql.yaml /etc/grafana/provisioning/datasources/
COPY dashboard-terreno.yaml /etc/grafana/provisioning/dashboards/
COPY dashboard-terreno-example.json /var/lib/grafana/dashboards/
COPY dashboard-terreno-realtime.json /var/lib/grafana/dashboards/