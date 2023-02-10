import sys
import json
import schedule
import requests
import time
import msal

config = json.load(open(sys.argv[1]))
prev_status = None

app = msal.PublicClientApplication(config["client_id"], authority=config["authority"], )
result = None

def auth_check(app=app):
    global result
    accounts = app.get_accounts()
    if accounts:
        # Account(s) exists in cache, probably with token too. Let's try the first.
        result = app.acquire_token_silent(config["scope"], account=accounts[0])

    if not result:
        # No suitable token exists in cache. Let's get a new one via the device login flow
        flow = app.initiate_device_flow(scopes=config["scope"])
        if "user_code" not in flow:
            raise ValueError(
                "Fail to create device flow. Err: %s" % json.dumps(flow, indent=4))

        print(flow["message"])
        sys.stdout.flush()

        result = app.acquire_token_by_device_flow(flow)

def toggle_relay(state):
    url = "http://"+config["relay_ip"]+"/RELAY="+state.upper()
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as err:
        print ("Error connecting to relay:\n",err)

def poll_presence():
    auth_check()
    graph_data = requests.get(config["endpoint"],headers={'Authorization': 'Bearer ' + result['access_token']},).json()
    status = graph_data['activity']

    global prev_status

    if prev_status != status:
        if status == "InACall" or status == "Presenting":
            toggle_relay('on')
        else:
            toggle_relay('off')
        
        print('Status changed to', status)
        prev_status = status

def main_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every(10).seconds.do(poll_presence)
main_loop()