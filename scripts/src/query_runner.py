import requests
import time

# colocar token aqui
token = "KM4r0WcRDdbDewRvZ71dMEjG0kLky543xsx6"

headers = {"Authorization": "bearer ghp_"+token}

def run_query(query):
    request = requests.post('https://api.github.com/graphql',
                                    json={'query': query}, headers=headers)                        
    while request.status_code == 502:
        time.sleep(2)
        request = requests.post('https://api.github.com/graphql',
                                    json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))