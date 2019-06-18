DEPENDENCIES := docker
REMOTE := no
NETWORK := internal_network
export

.check-dependencies:
	$(foreach depen,$(DEPENDENCIES),\
		$(if $(shell which $(depen)),,$(error "Programa $(depen) no instalado.")))
.check-network:
ifeq ($(shell docker network ls | grep $(NETWORK) | wc -l), 0)
	docker network create $(NETWORK)
endif

.checks: .check-dependencies .check-network

%-run: .checks % %/Makefile
	@cd $* && $(MAKE) --no-print-directory run-lastest

%-build: .checks % %/Makefile
	@cd $* && $(MAKE) --no-print-directory build-lastest

%-create: .checks % %/Makefile
	@cd $* && $(MAKE) --no-print-directory create-lastest

%-load: .checks % %/Makefile
	@cd $* && $(MAKE) --no-print-directory load-lastest

%-log: % %/Makefile
	@cd $* && $(MAKE) --no-print-directory log-lastest

info:
	@echo "Hello World"

all: storage-build storage-run monitor-build listener-build monitor-run listener-run storage-create storage-load
