import random
import string
import uuid


def random_email() -> str:
    prefix = "".join(random.choices(string.ascii_lowercase, k=8))
    return f"test_{prefix}@example.com"


def random_string(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_uuid() -> str:
    return str(uuid.uuid4())


JOBS = [
    "QA Engineer",
    "Backend Developer",
    "Frontend Developer",
    "DevOps Engineer",
    "Data Analyst",
    "Product Manager",
]


def random_job() -> str:
    return random.choice(JOBS)
