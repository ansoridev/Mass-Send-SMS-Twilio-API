import json, sys, time, requests

openFile = open("settings.json", "r").read()
setting = json.loads(openFile)['settings']
body = json.loads(openFile)['body']

account_sid = setting['accountid']
auth_token = setting['token']
sender = setting['number']
log = setting['log']
messages = body['message']

client = (account_sid, auth_token)
apiDate = '2010-04-01'
url = f'https://api.twilio.com/{apiDate}/Accounts/{account_sid}/Messages.json'

def callbackCheck(sid):
    response = requests.get(f'https://api.twilio.com/{apiDate}/Accounts/{account_sid}/Messages/{sid}.json',  auth=client)
    return response.json()

def send():
    filename = input('List Number (*.txt) >>  ')
    f = open(filename, "r")

    for line in f:
        number = line.replace('\n', '')
        payload = (f"Body={messages}&From={sender}&To={number}")
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        message = requests.post(url, data=payload, auth=client, headers=headers)
        parse = json.loads(json.dumps(message.json()))

        if message.status_code == 400:
            respons = f"{number} is invalid - Not Delivered - {parse}"
        elif message.status_code == 201:
            sid = parse['sid']
            status = parse['status']

            if status == 'queued':
                time.sleep(1)
                parse = json.loads(json.dumps(callbackCheck(sid)))
                if parse['status'] == 'queued' or status == 'sent':
                    respons = f"Message to {number} has been delivered! - {parse['status']}"
                elif parse['status'] == 'delivered':
                    respons = f"Message to {number} has been delivered!"
                elif parse['status'] == 'undelivered':
                    respons = f"Message to {number} not delivered, maybe number is inactive!"
                else:
                    respons = f"Message to {number} has been delivered! - {parse['status']}"
            elif status == 'delivered' or status == 'sent':
                respons = f"Message to {number} has been delivered!"
            elif status == 'undelivered' or status == 'failed':
                respons = f"Message to {number} not delivered, maybe number is inactive!"
            else:
                respons = message.status_code
        print(respons)
        write = open(log, 'a')
        write.write(respons + '\n')
    print("===========================================")
    print("All task have been done. Thanks back again!")

def check():
    try:
        send()
    except:
        print("ERROR: Please check your filename is correct!")
        check()

send()