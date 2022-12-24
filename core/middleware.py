import requests
from django.http import HttpResponse

from core.redis_conn import r

allowed = {}
ALLOWED_REGION = ['DE']


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
    print(req)
    return req['country']
    # return req['region'] in ALLOWED_REGION


def process_ip(request) -> bool:
    ip = str(request.META.get("X-Forwarded-For"))  # nginx header

    print(ip)

    ip_data = r.get(ip)

    if ip_data:
        r.hincrby(name=f"ips:{ip}", key='c', amount=1)

    else:
        # if not in redis
        l = get_location(ip)

        data = {'l': l,
                'c': 1}
        r.hset(name=ip, mapping=data)

        if l in ALLOWED_REGION:
            return True
        else:
            return False


# pipe = client.pipeline()
# pipe.hset(key, mapping=your_object).expire(duration_in_sec).execute()
#
# # for example:
# pipe.hset(key, mapping={'a': 1, 'b': 2}).expire(900).execute()
# Note: Pipeline does not ensure atomicity.
