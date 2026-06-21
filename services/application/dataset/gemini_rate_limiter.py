import time
from threading import Lock
from loguru import logger


class RateLimiter:
    def __init__(self, max_requests: int, period: int):
        self.max_requests = max_requests
        self.period = period
        self.timestamps = []
        self.lock = Lock()

    def acquire(self):
        with self.lock:
            now = time.time()

            self.timestamps = [t for t in self.timestamps if now - t < self.period]

            if len(self.timestamps) >= self.max_requests:
                sleep_time = self.period - (now - self.timestamps[0]) + 1

                logger.warning(f"Rate limit reached. Sleeping {sleep_time:.1f}s")

                time.sleep(sleep_time)

                now = time.time()

                self.timestamps = [t for t in self.timestamps if now - t < self.period]

            self.timestamps.append(time.time())
