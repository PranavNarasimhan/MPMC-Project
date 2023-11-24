import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app=Flask(__name__)

@app.route("/sms", methods=['GET','POst'])

def sms_reply():
    resp=MessagingResponse()
    resp.message("Thank you for your help")
    return str(resp)
if __name__=="__main__":
    app.run(debug=True)
