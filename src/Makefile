DEPENDENCIES := docker
REMOTE := no
NETWORK := internal_network
export

.PHONY: monitor listener storage

.check-dependencies:
	$(foreach depen,$(DEPENDENCIES),\
		$(if $(shell which $(depen)),,$(error "Programa $(depen) no instalado.")))
.check-network:
	$(if $(shell docker network ls | grep $(NETWORK) | wc -l) == 0,
		docker network create $(NETWORK),)
.checks: .check-dependencies .check-network

%-run: .checks
%-run: % %/Makefile
	@cd $* && $(MAKE) --no-print-directory run-lastest

%-build: .checks
%-build: % %/Makefile
	@cd $* && $(MAKE) --no-print-directory build-lastest

%-create: .checks
%-create: % %/Makefile
ifeq(%, storage)
	@cd $* && $(MAKE) --no-print-directory create-lastest
endif

%-load: .checks
%-load: % %/Makefile
ifeq(%, storage)
	@cd $* && $(MAKE) --no-print-directory load-lastest
endif

info:
	@echo "Hello World"