import time
from src.utils.heartbeat import GenerateHeartbeat


i = 0
while i < 1000:
    GenerateHeartbeat()
    time.sleep(60)
    i += 1
    print(i)

