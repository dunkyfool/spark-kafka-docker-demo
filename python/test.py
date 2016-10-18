from pykafka.common import OffsetType
from pykafka import KafkaClient
import time


ZOOKEEPER='172.17.0.2:2181'
client = KafkaClient(hosts='172.17.0.2:9092')
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
while True:
    msg1 = consumer1.consume()
    print 'finish msg1'
    msg2 = consumer2.consume()
    print 'finsh msg2'
    print '1\t', msg1.value, msg1.offset, msg1.partition
    print '2\t', msg2.value, msg2.offset, msg2.partition
    time.sleep(10**-0.5)

consumer.stop()
#'''

#consumer.
#for msg in consumer:
#    if msg is not None:
#        print msg.offest, msg.value
