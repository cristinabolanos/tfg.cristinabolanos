PASSWORD :=

%-lastest: MONITOR = grafana
%-lastest: VERSION = lastest
%-lastest: .%
	@echo "Done"

.ask-password:
ifeq ($(PASSWORD), )
	$(eval PASSWORD := $(shell bash -c 'read -s -p "Contraseña del administrador de grafana: " pwd; echo $$pwd'))
	@echo ""
endif

.build:
ifeq ($(REMOTE), no)
	@docker build -t=local/monitor/$(MONITOR):$(VERSION) .
else
	@docker build -t=$(REPOSITORY)/monitor/$(MONITOR):$(VERSION) .
	@docker push $(REPOSITORY)/monitor/$(MONITOR):$(VERSION)
endif

.run: .ask-password
ifeq ($(REMOTE), no)
ifneq ($(shell docker container ls | grep local_$(MONITOR) | wc -l), 0)
	@docker stop local_$(MONITOR)
endif
ifneq ($(shell docker ps -a | grep local_$(MONITOR) | wc -l), 0)
	@docker rm local_$(MONITOR)
endif
	@docker run -d -p 80:3000 --name=local_$(MONITOR) --network=$(NETWORK) -e "GF_SECURITY_ADMIN_PASSWORD=$(PASSWORD)" local/monitor/$(MONITOR):$(VERSION)
endif

.log:
ifeq ($(REMOTE), no)
	@docker logs local_$(MONITOR) | less
endif
