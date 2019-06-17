DROP USER IF EXISTS 'grafana'@'%';

CREATE USER 'grafana'@'%' IDENTIFIED BY 'secret';
GRANT SELECT ON example.* TO 'grafana'@'%';

DROP USER IF EXISTS 'listener'@'%';

CREATE USER 'listener'@'%' IDENTIFIED BY 'secret';
GRANT INSERT ON example.* TO 'listener'@'%';