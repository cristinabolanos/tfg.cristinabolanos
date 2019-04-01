
PASSWORD := secret

.check-dependencies:
	$(foreach depen,$(DEPENDENCIES),\
		$(if $(shell which $(depen)),,$(error "Programa $(depen) no instalado.")))

%-lastest: %-0.0.0
	@echo ""

%-0.0.0: MONITOR = grafana
%-0.0.0: VERSION = 0.0.0
%-0.0.0: .check-dependencies .%
	@echo "Software version: $(VERSION)"

.build:
ifeq ($(REMOTE), no)
	@docker build -t=local/monitor/$(MONITOR):$(VERSION) .
else
	@docker build -t=$(REPOSITORY)/monitor/$(MONITOR):$(VERSION) .
	@docker push $(REPOSITORY)/monitor/$(MONITOR):$(VERSION)
endif

.run:
ifeq ($(REMOTE), no)
	@docker run -d -p 80:3000 --name=local_$(MONITOR) --network=SUBI -e "GF_SECURITY_ADMIN_PASSWORD=$(PASSWORD)" local/monitor/$(MONITOR):$(VERSION)
endif