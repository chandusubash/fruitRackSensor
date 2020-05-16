import sys
import json
import random
from random import randint
import datetime
# Present date
print(sys.argv[0])
currentTime = datetime.datetime.now()
#get the latest id used in the application
file = open('idGenerator.txt','r')
n = int(file.read())
file.close()
n=n+1
rackList = ["rackA"]
for _ in range(100) :
    for rack in rackList :
        dictRack = {     "id": n, "temperature": float(random.randrange(155, 400))/10 ,"Humidity" : randint(1, 100), "pathogenPresence" : randint(0, 10),"time" : currentTime.strftime("%m-%d-%Y %H:%M:%S") }
        jsonRack = json.dumps(dictRack)
        print(jsonRack)
        # Writing to sample.json
        with open(rack+'/NE'+str(n)+'.json', 'w') as outfile:
            outfile.write(jsonRack)
        n=n+1

with open('idGenerator.txt','w') as file:
    file.write(str(n))
