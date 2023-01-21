import datetime as dt
import pytz

def get_wday_percent():
    # tz = pytz.timezone('Europe/Moscow')
    tz = pytz.timezone('Asia/Yekaterinburg')
    now = dt.datetime.now(tz=tz)
    d_start = now.replace(hour=10, minute=0, second=0)
    d_end = now.replace(hour=18, minute=0, second=0)
    d_len = d_end - d_start
    # print(d_len)

    if d_start < now < d_end:
        d = (now - d_start).seconds
        return round(d / d_len.seconds * 100)
    else:
        return 0