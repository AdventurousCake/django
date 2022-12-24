import logging

import requests
from django.http import HttpResponse

from core.redis_conn import r

allowed = {}
ALLOWED_REGION = ['RU']


def simple_ip_check(get_response):
    # one time
    # for each request

    # if not IS_SERVER:

    def middleware(request):
        # todo TRY
        if process_ip(request):
            response = get_response(request)
            return response
        else:
            return HttpResponse(status=444)

    return middleware


def get_location(ip):

    req = requests.get(f'https://ipinfo.io/{ip}', timeout=150).json()
    return req['country']
    # return req['region'] in ALLOWED_REGION


def process_ip(request) -> bool:
    ip = str(request.META.get("HTTP_X_FORWARDED_FOR"))  # nginx header

    if len(ip) > 15:
        logging.info('TWO IP X-Forwarded-For')
        ip = ip.split(',')[0]

    key = f"ips:{ip}"
    ip_data = r.hgetall(key)
    if ip_data:
        r.hincrby(name=key, key='c', amount=1)
        l = ip_data.get('l')

    else:
        print('new ip')
        # if not in redis
        l = get_location(ip)

        data = {'l': l,
                'c': 1}
        r.hset(name=key, mapping=data)

    if l in ALLOWED_REGION:
        return True
    else:
        print(f'ip block for: {ip}, {l}')
        logging.info(f'ip block for: {ip}, {l}')
        return False


# pipe = client.pipeline()
# pipe.hset(key, mapping=your_object).expire(duration_in_sec).execute()
#
# # for example:
# pipe.hset(key, mapping={'a': 1, 'b': 2}).expire(900).execute()
# Note: Pipeline does not ensure atomicity.
