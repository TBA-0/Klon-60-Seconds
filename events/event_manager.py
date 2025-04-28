import random
from events.event_pool import event_pool

def get_random_event():
    return random.choice(event_pool)
