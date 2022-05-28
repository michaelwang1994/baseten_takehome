import traceback

import os
from redis import Redis
from typing import Dict, Tuple

from configs import create_logger

logger = create_logger(__name__)


def create_redis_client():
    return Redis(
        host=os.environ['REDIS_HOST'],
        port=int(os.environ['REDIS_PORT']),
        db=0,
        charset="utf-8",
        decode_responses=True
    )


def store(redis_db: Redis, ip: str, document: Dict) -> bool:
    try:
        new_id = redis_db.incr(f'hset:invocations:ip:{ip}:id:', 1)
        new_key = f'hset:invocations:ip:{ip}:id:{new_id}'
        redis_db.hset(new_key, mapping=document)
        for key, value in document.items():
            redis_db.zadd(f'hset:invocations:ip:{ip}.{key}.index', {new_id: value})
        return True
    except Exception:
        logger.error(traceback.print_exc())
        return False


def get(redis_db: Redis, ip: str, value_ranges: Dict[str, Tuple[float]] = None):
    base_key = f'hset:invocations:ip:{ip}'
    ids = None
    for key, value_range in value_ranges.items():
        zrange_key = f'{base_key}.{key}.index'
        matched_ids = redis_db.zrangebyscore(zrange_key, value_range[0], value_range[1])
        if ids is None:
            ids = set(matched_ids)
        else:
            ids.intersection_update(set(matched_ids))
    results = []
    for i in ids:
        key_with_id = f'{base_key}:id:{i}'
        results.append(redis_db.hgetall(key_with_id))
    return results
