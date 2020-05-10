# main.py
import os,re,json,requests
url="https://a2fl82ml5m7c6e-ats.iot.us-east-1.amazonaws.com:8443/topics/data/"
rackList = ["rackA","rackB","rackC","rackD","rackE"]
for rack in rackList :
    fileArr = os.listdir(rack+'/')
    for file in fileArr :
        if re.match('NE',file) :
            #print(file)
            fileContent = open(rack+'/'+file,'r')
            #print(fileContent.read())
            fileJson=json.loads(fileContent.read())
            fileContent.close()
            print(fileJson["id"])
            os.rename(r''+rack+'/'+file,r''+rack+'/IE'+str(fileJson["id"])+'.json')
            headers = {'content-type': 'application/json'}
            request = requests.post(url+rack+'/'+str(fileJson["id"])+'?qos=1', data = json.dumps(fileJson),headers=headers, cert=('bf0d06941b-certificate.pem.crt', 'bf0d06941b-private.pem.key'), verify='AmazonRootCA1.pem.txt')
            print(request.status_code)
            os.rename(r''+rack+'/IE'+str(fileJson["id"])+'.json',r''+rack+'/CE'+str(fileJson["id"])+'.json')
