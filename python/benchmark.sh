#!/bin/sh

####################################
#          Default Setup           #
####################################
if [ "$1" = "START" ];then
	# Setup test1
	docker exec test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-topics.sh \
	--create \
	--zookeeper localhost:2181 \
	--replication-factor 1 \
	--partitions 1 \
	--topic test1
	# Setup test2
	docker exec test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-topics.sh \
	--create \
	--zookeeper localhost:2181 \
	--replication-factor 1 \
	--partitions 6 \
	--topic test2
	# List topic(s)
	docker exec test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-topics.sh \
	--list \
	--zookeeper localhost:2181 
	# Show detail of topic(s)
	# test1
	docker exec test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-topics.sh \
	--describe \
	--zookeeper localhost:2181 \
	--topic test1
	# test2
	docker exec test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-topics.sh \
	--describe \
	--zookeeper localhost:2181 \
	--topic test2
fi

####################################
#              Main                #
####################################
echo 'Enter an option as following.'
echo '0) Check current topic'
echo '1) 50M Producer'
echo '2) 50G Producer (Think twice before you choose it!!)'
echo '3) 10-10^5 Producer (Think twice before you choose it!!)'
echo '4) 50M Consumer'
echo '5) End2End Lantency'
#echo '4) '

read NUM
case $NUM in
	# List topic(s)
	0) \
	docker exec test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-topics.sh \
	--list \
	--zookeeper localhost:2181 
	# Show detail of topic(s)
	docker exec test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-topics.sh \
	--describe \
	--zookeeper localhost:2181 \
	--topic test1
	docker exec test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-topics.sh \
	--describe \
	--zookeeper localhost:2181 \
	--topic test2
	;;

	1) \
	echo \
	'############ Test1 ############'
	docker exec -it test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance \
	test1 50000000 100 -1 acks=1 bootstrap.servers=localhost:9092 buffer.memory=67108864 batch.size=8196
	: '
	  topic num_record size_record[byte] throughput{value>0; control sleep time}
	'
	echo \
	'############ Test2 ############'
	docker exec -it test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance \
	test2 50000000 100 -1 acks=1 bootstrap.servers=localhost:9092 buffer.memory=67108864 batch.size=8196
	;;

	2) \
	echo \
	'############ Test1 ############'
	docker exec -it test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance \
	test1 50000000000 100 -1 acks=1 bootstrap.servers=localhost:9092 buffer.memory=67108864 batch.size=8196
	echo \
	'############ Test2 ############'
	docker exec -it test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance \
	test2 50000000000 100 -1 acks=1 bootstrap.servers=localhost:9092 buffer.memory=67108864 batch.size=8196
	;;

	3) \
	for i in 10 100 1000 10000 100000;
	do
		echo ""
		echo $i

		echo '############ Test1 ############'
		docker exec -it test_kafka \
		/opt/kafka_2.11-0.8.2.1/bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance \
		test1 $((1000*1024*1024/$i)) $i -1 acks=1 bootstrap.servers=localhost:9092 buffer.memory=67108864 batch.size=128000

		echo '############ Test2 ############'
		docker exec -it test_kafka \
		/opt/kafka_2.11-0.8.2.1/bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance \
		test2 $((1000*1024*1024/$i)) $i -1 acks=1 bootstrap.servers=localhost:9092 buffer.memory=67108864 batch.size=128000
	done;
	;;

	4) \
	echo '############ Test1 ############'
	docker exec  -it test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-consumer-perf-test.sh \
	--zookeeper localhost:2181 --messages 50000000 --topic test1 --threads 1
	echo '############ Test2 ############'
	docker exec  -it test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-consumer-perf-test.sh \
	--zookeeper localhost:2181 --messages 50000000 --topic test2 --threads 1
	;;


	5) \
	echo '############ Test1 ############'
	docker exec  -it test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-run-class.sh kafka.tools.TestEndToEndLatency localhost:9092 localhost:2181 test1 5000 1 1
	echo '############ Test2 ############'
	docker exec  -it test_kafka \
	/opt/kafka_2.11-0.8.2.1/bin/kafka-run-class.sh kafka.tools.TestEndToEndLatency localhost:9092 localhost:2181 test2 5000 1 1
	;;

	#3) docker exec -it test_kafka \
	#/opt/kafka_2.11-0.8.2.1/bin/
	#;;
esac
