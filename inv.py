# Run for dev environments only as the http methods for delete/put/patch could destroy or alter data
# This has no warranties
#
# USING THIS SCRIPT COULD BE CONSIDERED PEN TESTING SO MAKE SURE YOU HAVE THE AUTHORITY IN
# TO RUN THIS SCRIPT AGAINST THE ENDPOINTS IN CSV
#
#Any of these could alter data especially the DELETE/PUT/PATCH
#
#
# Patrick McBrien 2023

#EXPECTED HEADER COLUMNS IN CSV ARE \ufeff"Host", Path, Method.

import csv
import requests
import lxml.html

def send_request(url, method):

        timeout = 3

        get=1
        post=0
        delete=0 #set to 1 to send HTTP delete's (this could alter data)
        put=0#set to 1 to put (this could alter data)
        patch=0#set to 1 patch (this could alter data)
        
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
                print ("HTML RESPONSE FOUND. Likely not insecure. Print first 20 chars")
                print(response.text[:20])

        except:
            pass

def main():
    csv_file = 'hosts.csv'
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


