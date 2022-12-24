from django1.settings import IS_SERVER
import redis

if IS_SERVER:
    r = redis.Redis(host='localhost', port=6379, db=0)
else:
    r = None
