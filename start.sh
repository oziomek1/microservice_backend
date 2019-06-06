#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'

help(){
	for a in $@; do
		if [[ $a == "-h" || $a == "--help" ]]
		then
			echo ""
			printf "${RED}HELP${NC}\n\n"
			echo $'flag -test run all tests\nflag -recreate recreates database and seed it with example data\nflag -stop stops containers\n\nIf you won`t use any flag it will build containers, start them and seed the database\n'
			exit 0
		fi
	done
}

checkFlags(){
	for a in $@; do
		if [[ $a == "-recreate" ]]
		then
			recreate="yes"
		fi
		if [[ $a == "-test" ]]
		then
			test="yes"
		fi
		if [[ $a == "-stop" ]]
		then
			stop="yes"
		fi
	done
}

test=""
recreate=""
stop=""

help $@
checkFlags $@

if [[ $test == "yes" ]]
then
	printf "${RED}Backend starts...${NC}\n"
	docker-compose -f docker-compose-dev.yml build
	docker-compose -f docker-compose-dev.yml up -d --build
	echo "Tests start"
	docker-compose -f docker-compose-dev.yml run backend python manage.py test
	docker-compose -f docker-compose-dev.yml run backend python manage.py test_coverage
	docker-compose -f docker-compose-dev.yml run backend flake8 project
	echo "Container go to sleep"
	docker-compose -f docker-compose-dev.yml stop
	printf "${RED}Everything is done...${NC}\n"
	exit 0
elif [[ $recreate == "yes" ]]
then
	printf "${RED}Recreate database...${NC}\n"
	docker-compose -f docker-compose-dev.yml run backend python manage.py recreate_db
	docker-compose -f docker-compose-dev.yml run backend python manage.py seed_db
	printf "${RED}Everything is done...${NC}\n"
	exit 0
elif [[ $stop == "yes" ]]
then
	printf "${RED}Container go to sleep${NC}\n"
	docker-compose -f docker-compose-dev.yml stop
	printf "${RED}Everything is done...${NC}\n"
	exit 0
else
	printf "${RED}Backend starts...${NC}\n"
	docker-compose -f docker-compose-dev.yml build
	docker-compose -f docker-compose-dev.yml up -d --build
	docker-compose -f docker-compose-dev.yml run backend python manage.py recreate_db
	docker-compose -f docker-compose-dev.yml run backend python manage.py seed_db
	printf "${RED}Everything is done...${NC}\n"
fi
