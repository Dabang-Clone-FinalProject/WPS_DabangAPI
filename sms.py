from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

# set api key, api secret
api_key = "NCSGLMHSQ2FTVZUA"
api_secret = "LCSOKSWPDNLZF971PMZ4XAQPZPYD60EW"

## 4 params(to, from, type, text) are mandatory. must be filled
params = dict()
params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
params['to'] = '01053487869'  # Recipients Number '01000000000,01000000001'
params['from'] = '01044321237'  # Sender number
params['text'] = 'RoomOption Message'  # Message

cool = Message(api_key, api_secret)
try:
    response = cool.send(params)
    print("Success Count : %s" % response['success_count'])
    print("Error Count : %s" % response['error_count'])
    print("Group ID : %s" % response['group_id'])

    if "error_list" in response:
        print("Error List : %s" % response['error_list'])

except CoolsmsException as e:
    print("Error Code : %s" % e.code)
    print("Error Message : %s" % e.msg)


test    