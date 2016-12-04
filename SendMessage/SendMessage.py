from twilio.rest import TwilioRestClient 
 
ACCOUNT_SID = "ACb6d473cb551965a4a98c76928d9abe66" 
AUTH_TOKEN = "591d13c644fc27af276d972990a822d4" 
def sendMessage(mediaURL):
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
    client.messages.create(
        to="+13605359123", 
        from_="+19284874422 ", 
        media_url=mediaURL, 
    )    
    return  
