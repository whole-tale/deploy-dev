#!/bin/bash

DONE=0
COUNT=0

echo -n "Removing volumes wt_mongo-cfg and wt_mongo-data..."

while [ "$DONE" == "0" ]; do
	OUT=`docker volume rm wt_mongo-cfg wt_mongo-data 2>&1`
	EC=$?
	if [ "$EC" == "0" ]; then
		echo " DONE"
		DONE=1
	else
		if [[ $OUT == *"volume is in use"* ]]; then
			COUNT=$(($COUNT + 1))
			if [ "$COUNT" -ge "10" ]; then
				echo
				echo "Mongo volumes wt_mongo-cfg and wt_mongo-data still in use after 20s. Please remove them manually."
				exit 1
			fi
			sleep 2
			echo -n "."
		else
			echo
			echo "Docker error: $OUT"
			exit $EC
		fi
	fi
done
