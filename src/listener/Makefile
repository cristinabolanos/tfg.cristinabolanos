
%-lastest: LISTENER = python
%-lastest: VERSION = lastest
%-lastest: .%
	@echo "Done"

.build:
ifeq ($(REMOTE), no)
	@docker build -t=local/listener/$(LISTENER):$(VERSION) .
else
	@docker build -t=$(REPOSITORY)/listener/$(LISTENER):$(VERSION) .
	@docker push $(REPOSITORY)/listener/$(LISTENER):$(VERSION)
endif

.run:
ifeq ($(REMOTE), no)
	@docker run -d -p 5009:5009 --name=local_$(LISTENER) --network=$(NETWORK) local/listener/$(LISTENER):$(VERSION)
endif