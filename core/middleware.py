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


def get_data(ip):
    req = requests.get(f'https://ipinfo.io/{ip}', timeout=150).json()  # or https://ipapi.co/
    return {'c': req['country'],
            'org': req['org']
            }
    # return req['region'] in ALLOWED_REGION


def process_ip(request) -> bool:
    ip = str(request.META.get("HTTP_X_FORWARDED_FOR"))  # nginx header

    if len(ip) > 15:
        # '1.2.3.4, 176.222.444.555' - last is real; or use 'x-real-ip'
        logging.info('TWO IP X-Forwarded-For')
        ip = ip.strip().split(',')[-1]

    key = f"ips:{ip}"
    ip_data = r.hgetall(key)
    if ip_data:
        r.hincrby(name=key, key='c', amount=1)
        location = ip_data.get('l')

    else:
        # if not in redis
        new_data = get_data(ip)
        location = new_data['c']

        data = {'l': location,
                'c': 1}
        r.hset(name=key, mapping=data)
        print(f'new ip: {ip} | {location} | {new_data.get("org")}')

    if location in ALLOWED_REGION:
        return True
    else:
        print(f'ip block for: {ip}, {location}')
        logging.info(f'ip block for: {ip}, {location}')
        return False

# pipe = client.pipeline()
# pipe.hset(key, mapping=your_object).expire(duration_in_sec).execute()
#
# # for example:
# pipe.hset(key, mapping={'a': 1, 'b': 2}).expire(900).execute()
# Note: Pipeline does not ensure atomicity.
