export DEPENDENCIES := docker docker-compose

.PHONY:

%-dev: %/Makefile

%-build: % %/Makefile
	@cd $* && $(MAKE) --no-print-directory build-lastest

info:
	@echo "Last version of software: 1.0.0"