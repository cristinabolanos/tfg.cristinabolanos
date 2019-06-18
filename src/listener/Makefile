
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
ifneq ($(shell docker container ls | grep local_$(LISTENER) | wc -l), 0)
	@docker stop local_$(LISTENER)
endif
ifneq ($(shell docker ps -a | grep local_$(LISTENER) | wc -l), 0)
	@docker rm local_$(LISTENER)
endif
	@docker run -d -p 5009:5009 --name=local_$(LISTENER) --network=$(NETWORK) local/listener/$(LISTENER):$(VERSION)
endif
