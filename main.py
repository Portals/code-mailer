#

import json
import requests

debug = False

# Add your secret gotify shared key
gotify_shared_key = 'SECRET'

with open('codes.json') as f:
    codes = json.load(f).get('codes')

with open('input.txt') as f:
    inputEmails = [line.rstrip() for line in f]

with open('sent.txt') as f:
    sentEmails = [line.rstrip() for line in f]

toSendEmail = [email for email in inputEmails if email not in sentEmails]
allSentEmails = toSendEmail + sentEmails

if not debug:
    with open('input.txt', 'w') as f:
        f.write('')

headers = {'Content-type': 'application/json',
           'Authorization': 'pre-shared: {}'.format(gotify_shared_key)}

url = 'https://gotify.chalmers.it/mail'


def send_email(email, user_codes):
    if not email:
        return

    post_fields = {
        "to": email,
        "from": "no-replay@chalmers.it",
        "subject": "Codes for VoteIT session, please keep safe",
        "body": "Your codes for this VoteIT session. Please keep safe and do not share with anyone\n\n" + "".join(
            ["{}: {}\n".format(i + 1, code) for i, code in enumerate(user_codes)])
    }

    if not debug:
        response = requests.post(url, data=json.dumps(post_fields), headers=headers)
        if (response.status_code != 200):
            print('{} failed to send code to. Code {}.'.format(email, response.status_code))
            print('Readding codes to codes...')
            codes.append(user_codes)
        else:
            print('{} was sent codes'.format(email))


for email in toSendEmail:
    send_email(email, codes.pop(0))

if not debug:
    with open('sent.txt', 'w') as f:
        for email in allSentEmails:
            f.write("{}\n".format(email))

new_codes = {
    "codes": codes
}

if not debug:
    with open('codes.json', 'w', encoding='utf-8') as f:
        json.dump(new_codes, f, ensure_ascii=False, indent=4)

print("Done")
