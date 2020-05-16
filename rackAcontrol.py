# -*- coding: utf-8 -*-

from time import sleep
import sys
import random
import cloud4rpi
import os,re,json,requests


#import ds18b20
#import rpi
#import RPi.GPIO as GPIO  # pylint: disable=F0401

# Put your device token here. To get the token,
# sign up at https://cloud4rpi.io and create a device.
DEVICE_TOKEN = 'XXXXXXXXXXXXXX'
url="https://a2fl82ml5m7c6e-ats.iot.us-east-1.amazonaws.com:8443/topics/data/"

# Constants
LED_PIN = 12
# Change these values depending on your requirements.
DATA_SENDING_INTERVAL = 60  # secs
DIAG_SENDING_INTERVAL = 650  # secs
POLL_INTERVAL = 0.5  # 500 ms

LOCATIONS = [
    {'lat': 13.0017, 'lng': +77.6694},  # Bangalore
]

# Configure GPIO library
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(LED_PIN, GPIO.OUT)


# Handler for the button or switch variable
#def led_control(value=None):
#    GPIO.output(LED_PIN, value)
#    return GPIO.input(LED_PIN)

def get_id():
        rack='rackA'
        fileArr = os.listdir(rack+'/')
        for file in fileArr :
            if re.match('IE',file) :
                #print(file)
                fileContent = open(rack+'/'+file,'r')
                #print(fileContent.read())
                fileJson=json.loads(fileContent.read())
                fileContent.close()
                identifier=fileJson["id"]
        return identifier

def get_temperature():
        rack='rackA'
        fileArr = os.listdir(rack+'/')
        for file in fileArr :
            if re.match('IE',file) :
                #print(file)
                fileContent = open(rack+'/'+file,'r')
                #print(fileContent.read())
                fileJson=json.loads(fileContent.read())
                fileContent.close()
                temp=fileJson["temperature"]
        return temp

def get_humidity():
        rack='rackA'
        fileArr = os.listdir(rack+'/')
        for file in fileArr :
            if re.match('IE',file) :
                #print(file)
                fileContent = open(rack+'/'+file,'r')
                #print(fileContent.read())
                fileJson=json.loads(fileContent.read())
                fileContent.close()
                humid=fileJson["Humidity"]
        return humid

def get_pathogenpresence():
        rack='rackA'
        fileArr = os.listdir(rack+'/')
        for file in fileArr :
            if re.match('IE',file) :
                #print(file)
                fileContent = open(rack+'/'+file,'r')
                #print(fileContent.read())
                fileJson=json.loads(fileContent.read())
                fileContent.close()
                pathogen=fileJson["pathogenPresence"]
        return pathogen



def get_location():
    return random.choice(LOCATIONS)



def main():
    # Load w1 modules
    #ds18b20.init_w1()

    # Detect ds18b20 temperature sensors
    #ds_sensors = ds18b20.DS18b20.find_all()

    # Put variable declarations here
    # Available types: 'bool', 'numeric', 'string', 'location'
    rack='rackA'
    device = cloud4rpi.connect(DEVICE_TOKEN)
    diagnostics = {
        'CPU Temp': 33,
        'IP Address': "10.0.0.0",
        'Host': rack,
        'Operating System': "Linux",
        'Client Version:': cloud4rpi.__version__,
    }

    device.declare_diag(diagnostics)
    device.publish_diag()
    variables = {'id': {
        'type': 'numeric',
        'bind': get_id
    },
    # 'Outside Temp': {
    #     'type': 'numeric' if ds_sensors else 'string',
    #     'bind': ds_sensors[1] if ds_sensors else get_empty_value
    # },

     'temperature': {
         'type': 'numeric',
         'bind': get_temperature
         },
    'humidity': {
        'type': 'numeric',
        'bind': get_humidity
    },
    'pathogenPresence': {
        'type': 'numeric',
        'bind': get_pathogenpresence
        },
    'Location': {
        'type': 'location',
        'bind': get_location
        }
    }
    device.declare(variables)
    device.publish_config()
    sleep(1)

    fileArr = os.listdir(rack+'/')
    for file in fileArr :
        if re.match('NE',file) :
            #print(file)
            fileContent = open(rack+'/'+file,'r')
            #print(fileContent.read())
            fileJson=json.loads(fileContent.read())
            fileContent.close()
            #print(fileJson["id"])
            os.rename(r''+rack+'/'+file,r''+rack+'/IE'+str(fileJson["id"])+'.json')
            headers = {'content-type': 'application/json'}
            request = requests.post(url+rack+'/'+str(fileJson["id"])+'?qos=1', data = json.dumps(fileJson),headers=headers, cert=('bf0d06941b-certificate.pem.crt', 'bf0d06941b-private.pem.key'), verify='AmazonRootCA1.pem.txt')
            print(request.status_code)
            #os.rename(r''+rack+'/IE'+str(fileJson["id"])+'.json',r''+rack+'/CE'+str(fileJson["id"])+'.json')
            device.publish_data()
            os.rename(r''+rack+'/IE'+str(fileJson["id"])+'.json',r''+rack+'/CE'+str(fileJson["id"])+'.json')
            sleep(DATA_SENDING_INTERVAL)

    # Use the following 'device' declaration
    # to enable the MQTT traffic encryption (TLS).
    #
    # tls = {
    #     'ca_certs': '/etc/ssl/certs/ca-certificates.crt'
    # }
    # device = cloud4rpi.connect(DEVICE_TOKEN, tls_config=tls)




if __name__ == '__main__':
    main()
