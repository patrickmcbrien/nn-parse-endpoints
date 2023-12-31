# Run for dev environments only as the http methods for delete/put/patch could destroy or alter data
# This has no warranties
#
# USING THIS SCRIPT COULD BE CONSIDERED PEN TESTING SO MAKE SURE YOU HAVE THE AUTHORITY IN
# TO RUN THIS SCRIPT AGAINST THE ENDPOINTS IN CSV
# Patrick McBrien 2023
#
#Prereqs
#install or update your python3
#
#pip3 install requests
#pip3 install lxml
#
#Usage

#1. Export nn api inventory into a csv file from the UI. You can do this by right clicking on the API inventory table and exporting the data to CSV format. 
#2. Name the csv file export.csv and put it inside the same path as this python script
#3. Turn on "GET,POST,DELETE" or any other http methods you want to include in your attack. (be careful attacking production endpoints, it could destroy / alter data)
#4. run the script usually python3 inv.py or something similar

#EXPECTED HEADER COLUMNS IN CSV ARE \ufeff"Host", Path, Method. Note the special character starting with \u.

import csv
import requests
import lxml.html

#Attack params
get=1         #yes attack api's that are associated with GET requests
post=0                   #yes attack api's that are associated with POST method api calls (use caution)
delete=0                 #set to 1 to send HTTP delete's (this could delete data)
put=0                    #set to 1 to put (this could place data)
patch=0                  #set to 1 patch (this could alter data so test in lower environments)
timeout = 6 #how many seconds before giving up on the api request

def send_request(url, method):

        
        headers = {"Content-Type": "charset=utf-8",
                    "Transfer-Encoding": "chunked",
                    "User-Agent": "nn-inv.py API inventory script"
                  }
        
        try:
            if method.upper() == 'GET' and get==1:
                response = requests.get(url, timeout=timeout)
            elif method.upper() == 'POST' and post==1:
                response = requests.post(url, timeout=timeout)
            elif method.upper() == 'DELETE' and delete==1: #untested
                response = requests.delete(url, timeout=timeout) #untested
            elif method.upper() == 'PUT' and put==1: #untested
                response = requests.put(url, timeout=timeout) #untested
            elif method.upper() == 'PATCH' and patch==1: #untested
                response = requests.patch(url, timeout=timeout) #untested
            else:
                print(f"Unsupported or method turned off for : {method}")
                return
            print(f"Request to {url} ({method}) returned : {response.status_code}")
            
            if ( lxml.html.fromstring(response.text).find('.//*') == None ):
                #print ("NOT HTML")
                print(response.text)
            else:
                print ("HTML returned. Skipping.")
                print(response.text[:20])

        except:
            pass

def main():
    csv_file = 'export.csv'
    cnt=0
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cnt=cnt+1
            host = row['\ufeff"Host"']
            path = row['Path']
            method = row['Method']
            internetfacing = row['Internet Facing']
            
            print(f"Hitting API {host} {path} with a {method} Counter: " + str(cnt))
        
            if "HTTPS" in internetfacing:
                url = f"https://{host}{path}"
            else:
                url = f"http://{host}{path}"
            send_request(url, method)



if __name__ == '__main__':
    main()


