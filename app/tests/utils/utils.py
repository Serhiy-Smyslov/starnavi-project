import random
import string
from datetime import datetime, timedelta, timezone


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_int() -> int:
    return random.randrange(1, 1000)


def random_float() -> float:
    return random.uniform(10.5, 75.5)


def random_datetime() -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=random_int())
