import os
import sys
import time
import requests
import browser_cookie3

# CONSTANTS
DOMAIN_NAME = '.hoyolab.com'
ACT_ID = 'e202102251931481'
URL_GET_STATUS = 'https://hk4e-api-os.hoyolab.com/event/sol/info'
URL_SIGN = 'https://hk4e-api-os.hoyolab.com/event/sol/sign'

# REQUEST HEADER & PARAMS
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json;charset=utf-8',
    'Origin': 'https://webstatic-sea.mihoyo.com',
    'Connection': 'keep-alive',
    'Referer': f'https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id={ACT_ID}&lang=en-us',
}
params = (
    ('lang', 'en-us'),
    ('act_id', ACT_ID)
)
json = {
    'act_id': ACT_ID
}

# GET CHROME COOKIES
cookies = None
chromecookies = os.path.join(os.path.expandvars("%userprofile%"),"AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies")
cookies = browser_cookie3.chrome(cookie_file=chromecookies, domain_name=DOMAIN_NAME)
# cookies = browser_cookie3.load(domain_name=DOMAIN_NAME)

cookies_list = [ cookie.name for cookie in cookies ]
found = "account_id" in cookies_list

if not found:
    print("ERROR: LOGIN INFORMATION MISSING!!!")
    print("Please manually login to www.hoyolab.com in Google Chrome before trying again...")
    time.sleep(3)
    sys.exit()


def get_status():
    try:
        response = requests.get(
            URL_GET_STATUS,
            headers=headers,
            params=params,
            cookies=cookies
        )
        return response.json()['data']['is_sign']
    except Exception as e:
        print("ERROR:", e)
        return None


def sign():
    params = (
        ('lang', 'en-us'),
    )
    try:
        response = requests.post(
            URL_SIGN,
            headers=headers,
            params=params,
            cookies=cookies,
            json=json
        )
        print(response.json())
        return response.json()
    except Exception as e:
        print("ERROR:", e)
        return None


if __name__ == "__main__":
    if not get_status():
        sign()
        if get_status():
            print("Daily Check-In rewards has been successfully claimed!")
        else:
            print("ERROR: Unable to claim Daily Check-In rewards...")
    else:
        print("Daily Check-In rewards has already been claimed today!")
    time.sleep(3)
