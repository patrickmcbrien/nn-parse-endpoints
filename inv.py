# Run for dev environments only as the http methods for delete/put/patch could destroy or alter data
# This has no warranties
#
# USING THIS SCRIPT COULD BE CONSIDERED PEN TESTING SO MAKE SURE YOU HAVE THE AUTHORITY IN
# TO RUN THIS SCRIPT AGAINST THE ENDPOINTS IN CSV
#
# Patrick McBrien 2023

#EXPECTED HEADER COLUMNS IN CSV ARE \ufeff"Host", Path, Method.

import csv
import requests

def send_request(url, method):
    
        headers = {"Content-Type": "charset=utf-8",
                    "Transfer-Encoding": "chunked"
                  }

        try:
            if method.upper() == 'GET':
                response = requests.get(url, timeout=3)
            elif method.upper() == 'POST':
                response = requests.post(url, timeout=3)
            elif method.upper() == 'DELETE': #untested
                response = requests.delete(url, timeout=3) #untested
            elif method.upper() == 'PUT': #untested
                response = requests.put(url, timeout=3) #untested
            elif method.upper() == 'PATCH': #untested
                response = requests.patch(url, timeout=3) #untested
            else:
            #print(f"Unsupported method: {method}")
                return
            print("")
            print(f"Request to {url} ({method}) returned : {response.status_code}")
            print(response.text)
        except:
            pass
        
   
def main():
    csv_file = 'hosts.csv'

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            host = row['\ufeff"Host"']
            path = row['Path']
            method = row['Method']
            internetfacing = row['Internet Facing']

            if "HTTPS" in internetfacing:
                url = f"https://{host}{path}"
            else:
                url = f"http://{host}{path}"
            send_request(url, method)
            
            
            ##send_request(url, method)
            ##print(host)
            ##print(path)
if __name__ == '__main__':
    main()
