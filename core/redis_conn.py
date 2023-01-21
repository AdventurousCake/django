from django1.settings import IS_SERVER
import redis

if IS_SERVER:
    # decode_responses increase load to decode, instead default bytes
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
else:
    raise Exception('Using redis m not on server')
    # r = None
