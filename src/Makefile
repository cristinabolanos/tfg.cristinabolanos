VERSION := 0.0.0

ifeq ($(VERSION), 0.0.0)
include ./ibmcloud.mk
endif

DEPENDENCIES := docker docker-compose
REMOTE := no

export

.PHONY: monitor

%-dev: %/Makefile

%-run: % %/Makefile
	@cd $* && $(MAKE) --no-print-directory run-lastest

%-build: % %/Makefile
	@cd $* && $(MAKE) --no-print-directory build-lastest

%-create: % %/Makefile
	@cd $* && $(MAKE) --no-print-directory create-lastest

%-load: % %/Makefile
	@cd $* && $(MAKE) --no-print-directory load-lastest

stop-containers:
	@docker stop $$(docker ps -aq -f name=local)

remove-containers: stop-containers
	@docker rm -f $$(docker ps -aq -f name=local)

remove-images:
	@docker rmi -f $$(docker images -aq -f reference=local/*/*)

remove-all: remove-containers remove-images

info:
	@echo "Last version of software: 0.0.0"