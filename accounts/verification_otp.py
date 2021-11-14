import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def sendOTP(mobile):
    phone = "+91"+str(mobile)
    account_sid = 'ACa502c98f97522de04196a2f2551b0c7d'
    auth_token = '34edca6eae77b9bc17091e42685c64c2'
    client = Client(account_sid, auth_token)

    verification = client.verify \
                        .services('VAf01fa90ac9afb5f15f1cf18a84885f04') \
                        .verifications \
                        .create(to=phone, channel='sms')

    print(verification.status)


def checkOTP(mobile, otp):
    account_sid = 'ACa502c98f97522de04196a2f2551b0c7d'
    auth_token = '34edca6eae77b9bc17091e42685c64c2'
    client = Client(account_sid, auth_token)

    verification_check = client.verify \
                            .services('VAf01fa90ac9afb5f15f1cf18a84885f04') \
                            .verification_checks \
                            .create(to='+91'+mobile, code=otp)

    print(verification_check.status)
    if verification_check.status == 'approved':
        return True
    else:
        return False
    