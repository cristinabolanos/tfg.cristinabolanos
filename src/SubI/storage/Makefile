
PASSWORD := secret

.check-dependencies:
	$(foreach depen,$(DEPENDENCIES),\
		$(if $(shell which $(depen)),,$(error "Programa $(depen) no instalado.")))

%-lastest: %-0.0.0
	@echo ""

%-0.0.0: STORAGE = mysql
%-0.0.0: VERSION = 0.0.0
%-0.0.0: .check-dependencies .%
	@echo "Software version: $(VERSION)"

.build:
ifeq ($(REMOTE), no)
	@docker build -t=local/storage/$(STORAGE):$(VERSION) .
else
	@docker build -t=$(REPOSITORY)/storage/$(STORAGE):$(VERSION) .
	@docker push $(REPOSITORY)/storage/$(STORAGE):$(VERSION)
endif

.run:
ifeq ($(REMOTE), no)
	@docker run -d --name=local_$(STORAGE) --network=SUBI -e "MYSQL_ROOT_PASSWORD=$(PASSWORD)" local/storage/$(STORAGE):$(VERSION)
endif

.create:
ifeq ($(REMOTE), no)
	@cat ./users.sql | docker exec -i local_mysql mysql -uroot -p$(PASSWORD)
	@cat ./restore.sql | docker exec -i local_mysql mysql -uroot -p$(PASSWORD) -Dexample
endif

.load:
ifeq ($(REMOTE), no)
	@cat ./example.sql | docker exec -i local_mysql mysql -uroot -p$(PASSWORD) -Dexample
endif