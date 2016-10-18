import sys
import time
import pprint as pp

###################
# Global Variable #
###################
msg_count = 10000
msg_size = 100
msg_payload = ('kafkatest' * 20).encode()[:msg_size]
_topic = b'qq'
#print(msg_payload)
#print(len(msg_payload))

#bootstrap_servers = 'localhost:9092'
bootstrap_servers = '172.17.0.2:9092'

producer_timings = {}
consumer_timings = {}

def calculate_thoughput(timing, n_messages=1000000, msg_size=100):
    print("Processed {0} messsages in {1:.2f} seconds".format(n_messages,
                                                              timing))
    print("{0:.2f} MB/s".format((msg_size * n_messages)/timing/(1024*1024)))
    print("{0:.2f} Msgs/s".format(n_messages/timing))

# pykafka
def pykafka_test_p(use_rdkafka=False):
    from pykafka import KafkaClient

    client = KafkaClient(hosts=bootstrap_servers)
    topic = client.topics[_topic]
    producer = topic.get_producer(use_rdkafka=use_rdkafka)

    produce_start = time.time()
    for i in range(msg_count):
        producer.produce(msg_payload)

    producer.stop()
    return time.time() - produce_start

def pykafka_check_p():
    from pykafka import KafkaClient

    client = KafkaClient(hosts=bootstrap_servers)
    topic = client.topics[_topic]
    pp.pprint(topic.earliest_available_offsets())
    pp.pprint(topic.latest_available_offsets())

def pykafka_test_c(use_rdkafka=False):
    from pykafka import KafkaClient

    client = KafkaClient(hosts=bootstrap_servers)
    topic = client.topics[_topic]
    consumer = topic.get_simple_consumer(use_rdkafka=use_rdkafka)

    msg_consumed_count = 0

    consumer_start = time.time()
    while True:
        msg = consumer.consume()
        if msg: msg_consumed_count += 1
        if msg_consumed_count >= msg_count: break

    consumer.stop()
    return time.time() - consumer_start

if __name__=='__main__':
    arg_list = sys.argv
    if len(arg_list)==1:
            print 'python main.py MODE'
            print 'MODE:1 [Producer] pykafka test'
            print 'MODE:2 [Producer] pykafka check'
            print 'MODE:3 [Consumer] pykafka test'
    else:
        if   arg_list[1]=='1':
             producer_timings['pykafka_producer']=pykafka_test_p()
             calculate_thoughput(producer_timings['pykafka_producer'])
        elif arg_list[1]=='2':
             pykafka_check_p()
        elif arg_list[1]=='3':
             consumer_timings['pykafka_consumer']=pykafka_test_c()
             calculate_thoughput(consumer_timings['pykafka_consumer'])
