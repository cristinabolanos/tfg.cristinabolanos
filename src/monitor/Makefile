PASSWORD ?= $(shell bash -c 'read -s -p "Contraseña: " pwd; echo $$pwd')

%-lastest: MONITOR = grafana
%-lastest: VERSION = lastest
%-lastest: .%
	@echo "Done"

.build:
ifeq ($(REMOTE), no)
	@docker build -t=local/monitor/$(MONITOR):$(VERSION) .
else
	@docker build -t=$(REPOSITORY)/monitor/$(MONITOR):$(VERSION) .
	@docker push $(REPOSITORY)/monitor/$(MONITOR):$(VERSION)
endif

.run:
ifeq ($(REMOTE), no)
	@docker run -d -p 80:3000 --name=local_$(MONITOR) --network=$(NETWORK) -e "GF_SECURITY_ADMIN_PASSWORD=$(PASSWORD)" local/monitor/$(MONITOR):$(VERSION)
endif