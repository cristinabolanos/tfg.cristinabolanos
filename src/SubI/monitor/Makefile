
.default-env:

%-lastest: %-1.0.0
	@echo ""

%-1.0.0: MONITOR = grafana
%-1.0.0: VERSION = 1.0.0
%-1.0.0: .%
	@echo "Software version: 1.0.0"

.build:
	docker build -t=local/monitor/$(MONITOR):$(VERSION) .