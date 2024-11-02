from threading import Thread
from kafkafuncs import main as consume 
from kafkafuncs import initialize_database
from write_to_json import main as consume_json

initialize_database()

thread_a = Thread(target=consume)
thread_b = Thread(target=consume_json)

thread_a.start()
thread_b.start()

thread_a.join()
thread_b.join()