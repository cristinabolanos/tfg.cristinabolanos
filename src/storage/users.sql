DROP USER IF EXISTS 'grafana'@'%';

CREATE USER 'grafana'@'%' IDENTIFIED BY 'secret';
GRANT SELECT ON example.* TO 'grafana'@'%';