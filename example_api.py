import time

import redis
from random import randint


r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_usd_rate(n):
    number = randint(1, n)

    cached_val = r.get(f"usd_rate:{number}")
    time.sleep(2)

    if cached_val:
        return f"Взято з кешу {int(cached_val)}"
    else:
        r.setex(f"usd_rate:{number}", 10000, number)

    return number


for i in range(1, 10):
    print(get_usd_rate(12))

