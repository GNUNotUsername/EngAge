from random import randint, randrange
from datetime import datetime, timedelta
import numpy as np

START_DATE = datetime.strptime('1/1/2021 12:00 AM', '%m/%d/%Y %I:%M %p')
END_DATE = datetime.strptime('09/14/2022 11:59 PM', '%m/%d/%Y %I:%M %p')

STATES = [
    "QLD",
    "NSW",
    "VIC",
    "TAS",
    "SA",
    "NA",
    "WA",
    "ACT",
    "JBT"
]

LINES = []
with open("/home/terry/project/words") as f:
    for NUM_LINES, line in enumerate(f):
        LINES.append(line.strip())

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def gen_woop_state():
    score_integer = randint(0, 33)
    score_decimal = randint(0, 9)
    score_float = float(f"{score_integer}.{score_decimal}")
    state = STATES[randint(0, 8)]
    date = random_date(START_DATE, END_DATE)
    return score_float, state, date.date()

def gen_random_user():
    """
    Generate random users using words from file at given path.
    """
    user = {"username": "", "email": "", "password1": "", "password2": ""}
    user["username"] = user["email"] = LINES[randint(0, NUM_LINES)] + "@" + LINES[randint(0, NUM_LINES)] + ".com"
    user["password1"] = user["password2"] = LINES[randint(0, NUM_LINES)] + str(randint(0, NUM_LINES)) + LINES[randint(0, NUM_LINES)]
    return user

def woop_gen(seed):
    """
    Returns a woop score for a user based on their suburb.

    Generates a WOOP score based on a mean calculated from a string seed (suburb).
    Scores within each suburb will be normally distributed
    """
    WOOP_MIN = 0
    WOOP_MAX = 33
    mean = abs(hash(seed)) % (WOOP_MAX + 1)
    sig = 6.9 # this standard deviation works surprisingly well lol
    score = int(np.random.normal(mean, sig))
    if score < WOOP_MIN:
        return 2*WOOP_MIN - score
    if score > WOOP_MAX:
        return 2*WOOP_MAX - score
    return score


if __name__ == "__main__":
    pass
