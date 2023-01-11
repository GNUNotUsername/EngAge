import sys
from time import sleep
from requests import get, post
from datetime import datetime
from constants import INTERESTS

AUTH_TOKEN = "adf200c9c93c7f73cbdbeb5d45d79315e86bcf20"
ENDPOINT_BASE = "https://matthewhoffman.biz"
ENDPOINT_SS = f"/analysis/api-get-ss"
ENDPOINT_GEN = "/analysis/api-populate-db"
ENDPOINT_INTERESTS = "/push/api-push-interests"
ENDPOINT_TOKEN = "/auth/token-request/"
ENDPOINT_CREATE_ACC = "/account/api-create-account/"
ENDPOINT_CHANGE_PASSWORD = "/auth/api-change-password/"
ENDPOINT_PUSH_CONTACT = "/push/api-push-pending-contact/"
ENDPOINT_PUSH_CONFIRM_CONTACT = "/push/api-push-confirm-contact/"
ENDPOINT_FETCH_FRIENDS = "/fetch/api-fetch-contacts"
ENDPOINT_SEND_MESSAGE = "/push/api-push-new-message/"
ENDPOINT_FETCH_MESSAGES = "/fetch/api-fetch-ordered-messages"
ENDPOINT_FETCH_CHECKIN = "/fetch/api-fetch-last-checkin"

USER_NAME = "grannyd@systemd.com"
PASSWORD = "jeremiahjenkins"

HEADERS = {
    "Authorization": f"Token {AUTH_TOKEN}"
}

STATES = [
    "QLD",
    "NSW",
    "VIC",
    "TAS",
    "SA",
    "NA",
    "WA",
    "ACT"
]

QUERY_INTERVALS = {
    "state": [1, datetime.now()],
    "suburb": [1, datetime.now()],
    "billboard": [31, datetime.now()],
}

def get_api(req_type, data, date):
    return get(f"{ENDPOINT_BASE}{ENDPOINT_SS}", params={'type': req_type, 'data': data, 'date': date}, headers=HEADERS)

def query_states(date):
    state_responses = {}
    for state in STATES:
        state_responses[state] = get_api("state", state, date.strftime("%Y-%m-%d"))
    return state_responses

def get_token(username, password):
    data = {"username": username, "password": password}
    response = post(f"{ENDPOINT_BASE}{ENDPOINT_TOKEN}", json=data)
    print(response.text)

def generate_random(req_type, number):
    return get(f"{ENDPOINT_BASE}{ENDPOINT_GEN}", params={'type': req_type, 'number': number}, headers=HEADERS)

def populate_db():
    #get_token()
    print(make_account("terry@terry.com", "bartsimpson").text)
    data_payload = {"interests": []}
    for interest in INTERESTS:
        data_payload["interests"].append(interest[1])
    print(data_payload)
    response = post(f"{ENDPOINT_BASE}{ENDPOINT_INTERESTS}", data=data_payload, headers=HEADERS)
    print(response.text)

def make_account(username, password):
    return post(f"{ENDPOINT_BASE}{ENDPOINT_CREATE_ACC}", data={"username": username, "email": username, "password1": password, "password2": password, "state": "QLD", "suburb": "Ashgrove", "travel_dist": "5", "real_name": "jerryyy lol"})

def change_password(username, password):
    return post(f"{ENDPOINT_BASE}{ENDPOINT_CHANGE_PASSWORD}", data={"username": username, "password1": password, "password2": password}, headers=HEADERS)

def add_friend(username):
    return post(f"{ENDPOINT_BASE}{ENDPOINT_PUSH_CONTACT}", data={"user_2": username}, headers=HEADERS)

def confirm_friend(username, token):
    new_headers = HEADERS.copy()
    new_headers["Authorization"] = f"Token {token}"
    return post(f"{ENDPOINT_BASE}{ENDPOINT_PUSH_CONFIRM_CONTACT}", data={"user_1": username}, headers=new_headers)

def fetch_friends(token):
    new_headers = HEADERS.copy()
    new_headers["Authorization"] = f"Token {token}"
    return get(f"{ENDPOINT_BASE}{ENDPOINT_FETCH_FRIENDS}", headers=new_headers)

def fetch_messages():
    return get(f"{ENDPOINT_BASE}{ENDPOINT_FETCH_MESSAGES}", params={"start_date":"1970-01-01"}, headers=HEADERS)

def send_message(user_2, content, token):
    new_headers = HEADERS.copy()
    new_headers["Authorization"] = f"Token {token}"
    return post(f"{ENDPOINT_BASE}{ENDPOINT_SEND_MESSAGE}", data={"user_2": user_2, "content": content}, headers=new_headers)

def fetch_checkin(token):
    new_headers = HEADERS.copy()
    new_headers["Authorization"] = f"Token {token}"
    return get(f"{ENDPOINT_BASE}{ENDPOINT_FETCH_CHECKIN}", headers=new_headers)

def main():
    current_time = datetime.now()
    previous_time = current_time = datetime.now()
    first_run = True
    while True:
        current_time = datetime.now()
        for query in QUERY_INTERVALS:
            if (current_time - QUERY_INTERVALS[query][1]).days < QUERY_INTERVALS[query][0] and not first_run:
                continue
            if first_run:
                first_run = False
            if query == "state":
                response_data = query_states(current_time)
                for response_item in response_data:
                    actual_response = response_data[response_item]
                    if actual_response.status_code != 200:
                        print(f"Request Error: {actual_response.status_code}, {actual_response.text}")
                        continue
                    print(actual_response.json())
                QUERY_INTERVALS[query][1] = current_time
        sleep(5)

if __name__ == "__main__":
    if "-p" in sys.argv:
        populate_db()
        sys.exit()
    if "-c" in sys.argv:
        change_password("grannyd@systemd.com", "lennartXGranny")
        sys.exit()
    if "-r" in sys.argv:
        #print(make_account("adi@moe.com", "jeremiahjenkins").text)
        #print(get_token("adi@moe.com", "jeremiahjenkins"))
        print(make_account("test22211133@test.com", "jeremiahjenkins").text)
        #print(get_token("grannyd@sy1stemd.com", "jeremiahjenkins"))
        #print(get_token("test@test.com", "jeremiahjenkins"))
        sys.exit()
    if "-f" in sys.argv:
        print(add_friend("adi@moe.com").text)
        sys.exit()
    if "-cf" in sys.argv:
        print(confirm_friend("grannyd@systemd.com", "9dc58f5bca3423fd4e69b74e41da7b3214a5869c").text)
        sys.exit()
    if "-ff" in sys.argv:
        print(fetch_friends(AUTH_TOKEN).text)
        sys.exit()
    if "-sm" in sys.argv:
        print(send_message("adi@moe.com", """Ben Shapiro Attempts to Sing All Star:
Now, lets say, hypothetically, that somebody once told me that the world would proceed to roll me, and made the claim that I was not, the smartest tool in the shed. Which would lead us to look at the facts and see that she was looking kind of dumb, due to the fact that she had placed her finger and her thumb, in the shape of the letter L, located on her forehead.
This would mean that the years would start coming, and logically wont stop coming, that I was, hypothetically, fed to the rules, which would proceed with me hitting the ground running. Which didn’t make sense, to live for fun, in a way that your brain gets smart, yet your head gets dumb, seeing as there’s so much to do, and so much to see, so now I must pose the question, what is wrong with taking the backseat? This is due to the fact that you’ll never know if you don’t go, nor you will shine if you don’t glow.""", AUTH_TOKEN).text)
        sys.exit()
    if "-fm" in sys.argv:
        print(fetch_messages().text)
        sys.exit()
    if "-fci" in sys.argv:
        print(fetch_checkin(AUTH_TOKEN).text)
        sys.exit()
    main()
