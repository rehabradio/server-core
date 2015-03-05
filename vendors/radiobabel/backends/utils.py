# stdlib imports
import random


def random_pick(records, limit=10):
    top_picks = []
    for (i, record) in enumerate(records):
        if i >= limit:
            break
        top_picks.append(record)

    r_pick = random.choice(top_picks)

    return r_pick
