#!/bin/bash

source bin/activate
export FLASK_ENV=development
{
	./run.sh
} || {
	deactivate
}