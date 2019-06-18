
.check-dependencies:
	$(foreach depen,$(DEPENDENCIES),\
		$(if $(shell which $(depen)),,$(error "Programa $(depen) no instalado.")))

%-lastest: %-0.0.0
	@echo ""

%-0.0.0: LISTENER = python
%-0.0.0: VERSION = 0.0.0
%-0.0.0: .check-dependencies .%
	@echo "Software version: $(VERSION)"

.build:
ifeq ($(REMOTE), no)
	@docker build -t=local/listener/$(LISTENER):$(VERSION) .
else
	@docker build -t=$(REPOSITORY)/listener/$(LISTENER):$(VERSION) .
	@docker push $(REPOSITORY)/listener/$(LISTENER):$(VERSION)
endif

.run:
ifeq ($(REMOTE), no)
	@docker run -d -p 5009:5009 --name=local_$(LISTENER) --network=SUBI local/listener/$(LISTENER):$(VERSION)
endif