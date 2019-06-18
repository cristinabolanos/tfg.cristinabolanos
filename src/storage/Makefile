PASSWORD ?= $(shell bash -c 'read -s -p "Contraseña: " pwd; echo $$pwd')

%-lastest: STORAGE = mysql
%-lastest: VERSION = lastest
%-lastest: .%
	@echo "Done"

.build:
ifeq ($(REMOTE), no)
	@docker build -t=local/storage/$(STORAGE):$(VERSION) .
else
	@docker build -t=$(REPOSITORY)/storage/$(STORAGE):$(VERSION) .
	@docker push $(REPOSITORY)/storage/$(STORAGE):$(VERSION)
endif

.run:
ifeq ($(REMOTE), no)
	@docker run -d --name=local_$(STORAGE) --network=$(NETWORK) -e "MYSQL_ROOT_PASSWORD=$(PASSWORD)" local/storage/$(STORAGE):$(VERSION)
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