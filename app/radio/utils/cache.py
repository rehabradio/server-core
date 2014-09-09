# std-lib imports
import datetime


def build_key(*args):
    """Build a key for cached data, appends a timestamp onto each key."""
    cache_name = []
    for attr in args:
        cache_name.append(str(attr))
    cache_name.append(str(datetime.datetime.utcnow().strftime('%Y%m%d')))

    return '-'.join(cache_name)
