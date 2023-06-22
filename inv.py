# Run for dev environments only as the http methods for delete/put/patch (or others) could destroy or alter data
#
# This has no warranties
#
# USING THIS SCRIPT COULD BE CONSIDERED PEN TESTING SO MAKE SURE YOU HAVE THE AUTHORITY IN WRITING
# TO RUN THIS SCRIPT AGAINST THE ENDPOINTS IN CSV
#
# Patrick McBrien 2023

import csv
import requests

def send_request(url, method):
    if method.upper() == 'GET':
        response = requests.get(url)
    elif method.upper() == 'POST':
        response = requests.post(url)
    elif method.upper() == 'DELETE': #untested
        response = requests.delete(url) #untested
    elif method.upper() == 'PUT': #untested
        response = requests.put(url)  #untested
    elif method.upper() == 'PATCH': #untested
        response = requests.patch(url)  #untested
    else:
        #print(f"Unsupported method: {method}")
        return

    print("")
    print(f"Request to {url} ({method}) returned : {response.status_code}")
    print(response.text)
   
def main():
    csv_file = 'hosts.csv'

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            host = row['\ufeff"Host"']
            path = row['Path']
            method = row['Method']

            url = f"http://{host}/{path}"
            send_request(url, method)
            
            url = f"https://{host}/{path}"
            send_request(url, method)
            ##print(host)
            ##print(path)
if __name__ == '__main__':
    main()
