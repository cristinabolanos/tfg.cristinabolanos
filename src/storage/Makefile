PASSWORD :=

%-lastest: STORAGE = mysql
%-lastest: VERSION = lastest
%-lastest: .%
	@echo "Done"

.ask-password:
ifeq ($(PASSWORD), )
	$(eval PASSWORD := $(shell bash -c 'read -s -p "Contraseña de la base de datos: " pwd; echo $$pwd'))
	@echo ""
endif

.build:
ifeq ($(REMOTE), no)
	@docker build -t=local/storage/$(STORAGE):$(VERSION) .
else
	@docker build -t=$(REPOSITORY)/storage/$(STORAGE):$(VERSION) .
	@docker push $(REPOSITORY)/storage/$(STORAGE):$(VERSION)
endif

.run: .ask-password
ifeq ($(REMOTE), no)
ifneq ($(shell docker container ls | grep local_$(STORAGE) | wc -l), 0)
	@docker stop local_$(STORAGE)
endif
ifneq ($(shell docker ps -a | grep local_$(STORAGE) | wc -l), 0)
	@docker rm local_$(STORAGE)
endif
	@docker run -d --name=local_$(STORAGE) --network=$(NETWORK) -e "MYSQL_ROOT_PASSWORD=$(PASSWORD)" local/storage/$(STORAGE):$(VERSION)
endif

.create: .ask-password
ifeq ($(REMOTE), no)
	@cat ./users.sql | docker exec -i local_mysql mysql -uroot -p$(PASSWORD)
	@cat ./restore.sql | docker exec -i local_mysql mysql -uroot -p$(PASSWORD) -Dexample
endif

.load: .ask-password
ifeq ($(REMOTE), no)
	@cat ./example.sql | docker exec -i local_mysql mysql -uroot -p$(PASSWORD) -Dexample
endif

.log:
ifeq ($(REMOTE), no)
	@docker logs local_$(STORAGE) | less
endif
