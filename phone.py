#coding:utf-8#
from twilio.rest import Client
import time

# Your Account Sid and Auth Token from twilio.com/console
def main():
    accoundt_sid = 'AC7ea3e3001382b8a30a2c4773568621d3'
    auth_token = '1055b5b9f55f52f5c6c9a23520614f75'
    client = Client(accoundt_sid, auth_token)

    call = client.calls.create(
        url="https://demo.twilio.com/welcome/voice.xml",
        to='+8618130097619',#例如+8613512122323  要加国家码
        from_='+12058786366',#例如+1661491111   这个在账号里面去申请就好了
        #body='test info'
        )

    print(call.sid)
    #time.sleep(3.7)
    #call = client.calls(call.sid) \
     #            .update(status="completed")
    #print(call.to)
if __name__ == '__main__':
    for i in range(10):
        main()