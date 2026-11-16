from datetime import datetime, timedelta
from itertools import product
from random import Random

from src.users.constants import CITIES, NAMES, REGISTRATION_AGE_DAYS, SEGMENT_WEIGHTS
from src.users.exceptions import InvalidUserCountError
from src.users.models import User


def generate_users(count: int, rng: Random, now: datetime) -> list[User]:
    profiles = list(product(NAMES, CITIES))
    if not 1 <= count <= len(profiles):
        raise InvalidUserCountError(count=count, max_count=len(profiles))

    selected_profiles = rng.sample(profiles, count)
    segments = tuple(SEGMENT_WEIGHTS)
    weights = tuple(SEGMENT_WEIGHTS.values())
    users = []

    for user_id, (name, city) in enumerate(selected_profiles, start=1):
        segment = rng.choices(segments, weights=weights, k=1)[0]
        min_days, max_days = REGISTRATION_AGE_DAYS[segment]
        age_seconds = rng.randint(min_days * 86400 + 1, max_days * 86400)
        users.append(
            User(
                user_id=user_id,
                name=name,
                city=city,
                segment=segment,
                registered_at=now - timedelta(seconds=age_seconds),
            )
        )

    return users
