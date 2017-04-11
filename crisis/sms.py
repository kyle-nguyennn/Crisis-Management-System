from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def send_sms(contact, message):
    """
    Send sms to the given number
    :param message: The message to be sent to the number
    :return: None
    """

    #Zhenghao 8382 6317
    #Kyle 8591 0147
    account_sid = "ACcd667f6f6e95aac7ccca9b6e03638198"
    auth_token = "04bdceaf5721cbca7668b7da4212ea18"
    client = Client(account_sid, auth_token)

    try:
        client.messages.create(body=message, to="+65"+contact, from_="+13142000173")
        print("SMS has been sent to " + "+65"+contact)
        return True
    except TwilioRestException:
        return False