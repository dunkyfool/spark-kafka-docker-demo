from pykafka.common import OffsetType
from pykafka import KafkaClient
from pykafka.cli import kafka_tools
from argparse import Namespace
import time
import pprint as pp

ZOOKEEPER='172.20.0.2:2181'
client = KafkaClient(hosts='172.20.0.2:9092')
topic = client.topics['qq']


############
# PRODUCER #
############
'''
# async
start = time.time()
with topic.get_producer(delivery_reports=True) as producer:
    for i in range(5):
        producer.produce('test message'+str(i))

print 'async_time\t',time.time() - start
'''
'''
# sync
start = time.time()
with topic.get_sync_producer(delivery_reports=True) as producer:
    for i in range(5):
        producer.produce('test message'+str(i))

print 'sync_time\t',time.time() - start
'''

############
# CONSUMER #
############
#'''
#consumer = topic.get_simple_consumer(consumer_group='mygroup',
#                                     auto_offset_reset=OffsetType.EARLIEST,
#                                     auto_commit_enable=True,
#                                     auto_commit_interval_ms=10000,
#                                     reset_offset_on_start=False)

consumer1 = topic.get_balanced_consumer(consumer_group='mygroup',
                                     zookeeper_connect=ZOOKEEPER,
                                     auto_offset_reset=OffsetType.EARLIEST,
                                     auto_commit_enable=True,
                                     auto_commit_interval_ms=10000,
                                     reset_offset_on_start=False)

consumer2 = topic.get_balanced_consumer(consumer_group='mygroup',
                                     zookeeper_connect=ZOOKEEPER,
                                     auto_offset_reset=OffsetType.EARLIEST,
                                     auto_commit_enable=True,
                                     auto_commit_interval_ms=10000,
                                     reset_offset_on_start=False)
print 'step 1'

#consumer1.start()
#consumer2.start()

print 'start to roll'
ctr=0
while True:
    ctr+=1
    print ctr
    if ctr<20:
        msg1 = consumer1.consume()
        print 'finish msg1'
        msg2 = consumer2.consume()
        print 'finsh msg2'

        pp.pprint(consumer1.partitions)
        pp.pprint(consumer2.partitions)
        print '1\t', msg1.value, msg1.offset, msg1.partition
        print '2\t', msg2.value, msg2.offset, msg2.partition
        args= Namespace(topic='qq',consumer_group='mygroup')
        print kafka_tools.print_consumer_lag(client,args)
        time.sleep(10**-0.5)
    elif ctr==20:
        consumer2.stop()
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        print 'consumer stop'
        time.sleep(10**-0.5)
    elif ctr==30:
        consumer3 = topic.get_balanced_consumer(consumer_group='mygroup',
                                     zookeeper_connect=ZOOKEEPER,
                                     auto_offset_reset=OffsetType.EARLIEST,
                                     auto_commit_enable=True,
                                     auto_commit_interval_ms=10000,
                                     reset_offset_on_start=False)
        #consumer3.start()
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        print 'consumer3 start'
        time.sleep(10**-0.5)
    elif ctr>30:
        msg1 = consumer1.consume()
        print 'finish msg1'
        msg3 = consumer3.consume()
        print 'finsh msg3'

        pp.pprint(consumer1.partitions)
        pp.pprint(consumer2.partitions)
        pp.pprint(consumer3.partitions)
        print '1\t', msg1.value, msg1.offset, msg1.partition
        print '2\t', msg2.value, msg2.offset, msg2.partition
        print '3\t', msg3.value, msg3.offset, msg3.partition
        time.sleep(10**-0.5)
    elif ctr>20 and ctr<30:
        msg1 = consumer1.consume()
        print 'finish msg1'
        #msg2 = consumer2.consume()
        #print 'finsh msg2'

        pp.pprint(consumer1.partitions)
        pp.pprint(consumer2.partitions)
        print '1\t', msg1.value, msg1.offset, msg1.partition
        print '2\t', msg2.value, msg2.offset, msg2.partition
        time.sleep(10**-0.5)

consumer1.stop()
consumer2.stop()
#'''

#consumer.
#for msg in consumer:
#    if msg is not None:
#        print msg.offest, msg.value
