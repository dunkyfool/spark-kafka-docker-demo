#!/bin/sh

if [ "$1" = "spark" ];then
	docker exec -it test_spark bash
elif [ "$1" = "kafka" ];then
	docker exec -it test_kafka bash
elif [ "$1" = "" ];then
	echo "Usage ./enter.sh [kafka|spark]"
fi
