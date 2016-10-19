Please follow the article below to install requirement!!
https://roshansanthosh.wordpress.com/2016/02/23/apache-spark-pyspark-standalone-installation-on-ubuntu-14-04/

#Docker image
- ubuntu:toolkit (based on 16.04, pls refer to Dockerfile & toolkit-build.sh)
- antlypls/kafka:0.10.0.1
- antlypls/spark:1.6.2

#Start
1. Setup docker network & launch docker-compose
```
>> docker network create logging
>> ./launch.sh
```

2. Check the status of each container(test-spark,test-kafka,test-toolkit)
```
>> ./check.sh
```

3. Enter to container you want.
```
>> ./enter.sh [kafka|spark|toolkit]
```

4. After access toolkit container, go to /mnt folder. (default volume will mount .python/:/mnt )
```
>> ./enter.sh toolkit
```
5. Edit kafka server host in python/pc-check .py:line16 & python/test.py:line8-9
6. Open another terminal and access kafka container, and create qq topic with at least two partitions.
```
>> ./enter.sh kafka
# Create qq topic
>> kafka-topics.sh --create --topic qq --zookeeper $ZOOKEEPER --partitions 5 --replication-factor 1
# Check status
>> kafka-topics.sh --list --zookeeper $ZOOKEEPER
>> kafka-topics.sh --describe --zookeeper $ZOOKEEPER
```
7. Run pc-check.py first in order to insert 10000 msgs to qq topic 
```
# Insert
>> python pc-check.py 1
# Check
>> python pc-check.py 2
```
8. Run test.py in order to review how the balanced consumer work
```
>> python test.py
# During first 19 cycles, it will consume qq topic by two different consumer instances
# At 20 cycle, it will stop consumer instance No.2
# During 21 to 29 cycle, it still track both consumer instances' properties
# After 30 cycle, it will launch consumer instance No.3
```
