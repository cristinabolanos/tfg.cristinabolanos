# file: ibmcloud.mk --> Variables and targets IBM Cloud dependant make takes

#### VARIABLES

REPOSITORY := registry.eu-gb.bluemix.net/tfg-cristinabolanos-2019
API := https://api.eu-gb.bluemix.net
REGION := uk-south
CLUSTER := example-cluster
INSTALL = no

#### TARGETS
login:
	sudo ibmcloud login -a $(API) --apikey @apiKey.json
ifeq ($(INSTALL), yes)
	curl -sL https://ibm.biz/idt-installer | bash
	ibmcloud plugin install container-registry -r Bluemix
endif
	ibmcloud ks region-set $(REGION)
	ibmcloud ks cluster-config $(CLUSTER)