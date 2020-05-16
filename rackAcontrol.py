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
DEVICE_TOKEN = 'VGLWkPveLpUtRjrX8m9B7bmi'
#S3 bucket storage URL.
url="https://a2fl82ml5m7c6e-ats.iot.us-east-1.amazonaws.com:8443/topics/data/"

# Constants
DATA_SENDING_INTERVAL = 60  # secs

LOCATIONS = [
    {'lat': 13.0017, 'lng': +77.6694},  # Bangalore
]

# The funtion picks up the id value from the json saved in raspberry Pi.
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

# The funtion picks up the temperature value from the json saved in raspberry Pi.
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

# The funtion picks up the humidity value from the json saved in raspberry Pi.
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

# The funtion picks up the pathogen presence value from the json saved in raspberry Pi.
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


#Record the location of the sensor.
def get_location():
    return random.choice(LOCATIONS)



def main():
    #Configure the Rack information.
    rack='rackA'
    device = cloud4rpi.connect(DEVICE_TOKEN)

    #The gateway node diagnostics information.
    diagnostics = {
        'CPU Temp': 33,
        'IP Address': "10.0.0.0",
        'Host': rack,
        'Operating System': "Linux",
        'Client Version:': cloud4rpi.__version__,
    }
    device.declare_diag(diagnostics)
    device.publish_diag()

    #The individual node data.
    variables = {'id': {
        'type': 'numeric',
        'bind': get_id
    },
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
    # sleep for a second to make sure the configuration data is published.
    #Pick the jsons recorded by the sensor.
    fileArr = os.listdir(rack+'/')
    for file in fileArr :
        if re.match('NE',file) :
            #Load json file to a json dictionary
            fileContent = open(rack+'/'+file,'r')
            fileJson=json.loads(fileContent.read())
            fileContent.close()
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
