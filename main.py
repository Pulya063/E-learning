import random
import time
import multiprocessing as mp
from math import radians

import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def fib(n):
    if n <= 1: return n
    if n == 2: return 1

    cached = r.get(f"fib_sum:{n}")
    if cached:
        return int(cached)

    res = fib(n - 1) + fib(n - 2)

    r.setex(f"fib_sum:{n}", 3600, res)
    return res

def fib_nocache(n):
    if n <= 1: return n
    if n == 2: return 1

    res = fib_nocache(n - 1) + fib_nocache(n - 2)

    return res


def fib_with_cache(n):
    start = time.time()
    for i in range(1, n):
        number = random.randint(1, i)

        cached_val = r.get(f"fib_sum:{number}")

        if cached_val:
            result = int(cached_val)
        else:
            result = fib(number)

        r.setex(f"fib_sum:{number}", 3600, result)

    end = time.time()

    print(f"✅ (З КЕШЕМ) завершив за: {end - start:.4f} сек")

def fib_without_cache(n):
    start = time.time()

    for i in range(1, n):
        num = random.randint(1, i)

        result = fib_nocache(num)

    end = time.time()
    print(f"❌(БЕЗ КЕШУ) завершив за: {end - start:.4f} сек")

if __name__ == "__main__":
    cycles = 55

    r.flushall()

    print(f"Запуск обчислень числа фібоначі для чисел: від 1 до {cycles}\n")

    p1 = mp.Process(target=fib_with_cache, args=(cycles,))
    p2 = mp.Process(target=fib_without_cache, args=(cycles,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()