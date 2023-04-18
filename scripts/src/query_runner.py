import requests
import time 

# colocar token aqui
TOKEN = 0
TOKENS = ["eOVIR7AwkNb7mzKjuY4UoGSqedkBkL0dC4nu", "SAC5Cq2Apnat2W3JLQDH7l4mjfxK271beAHY"]



def run_query(query):
    global TOKEN
    headers = {"Authorization": "bearer ghp_"+TOKENS[TOKEN]}
    request = requests.post('https://api.github.com/graphql',
                                    json={'query': query}, headers=headers)                        
    ratelimitRemaining = request.headers.get('x-ratelimit-remaining')
    if ratelimitRemaining is not None: print('requests sobrando pro token: '+ratelimitRemaining)
    if not ratelimitRemaining and request.status_code in (403, 502):
        time.sleep(20)
        return run_query(query)
    if ratelimitRemaining <= '1':
        if TOKEN == 0: TOKEN = 1
        elif TOKEN == 1: TOKEN = 0
        return run_query(query)
    while request.status_code == 502:
        time.sleep(2)
        request = requests.post('https://api.github.com/graphql',
                                    json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))