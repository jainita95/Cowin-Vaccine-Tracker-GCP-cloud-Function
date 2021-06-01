# -*- coding: utf-8 -*-
"""
Created on Sat May  8 08:33:42 2021

@author: abc
"""


import requests
import json
from datetime import date
from twilio.rest import Client
import requests
from datetime import timedelta


def send_notification(response, contact_directory, district,day):
    response_dict = json.loads(response.content)
    sessions = response_dict['sessions']
    print(response_dict)
    message = "{} Vaccine Availability for district {} : ".format(day, district)
    count = 1
    for session in sessions:
        message = '{} \n {}- name : {} , pincode : {} , for age above : {} , availability : {} , avaiable vaccine : {}'.format(message,count ,session['name'],session['pincode'] ,session['min_age_limit'],session['available_capacity'] ,session['vaccine'] )
        count = count+1 

    if len(sessions)>0:
        twilio_sid = 'SID'
        auth_token = 'Token'
        whatsapp_client = Client(twilio_sid, auth_token)
        
        for key, value in contact_directory.items():
                msg_loved_ones = whatsapp_client.messages.create(
                        body = message,
                        from_= 'whatsapp:+14155238886',
                        to='whatsapp:' + value,

                        )
                
def call(request):                
    
    headers={'User-Agent': 'PostmanRuntime/7.26.8',
    'Accept': 'application/json',
    'Accept-Language': 'hi_IN',
    'Host': 'cdn-api.co-vin.in'}
    today = date.today().strftime("%d-%m-%Y")
    tomorrow = (date.today() + timedelta(days=1)).strftime("%d-%m-%Y")

    
    response_gondia = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=378&date={}".format(today),headers=headers,verify=False)
    response_gondia_tomorrow = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=378&date={}".format(tomorrow),headers=headers,verify=False)
    contact_directory_gondia = {'Jenu':'+91123456789'}
    
    send_notification(response_gondia,contact_directory_gondia, 'Gondia',"Today's")
    send_notification(response_gondia_tomorrow,contact_directory_gondia, 'Gondia',"Tomorrow's")
    
