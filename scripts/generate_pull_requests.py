
import pandas as pd
import datetime
import os
from src.query_runner import run_query
from src.queries import getPullRequestsQuery
import src.path as path



# le do csv de repositorios e itera sobre eles para consultar os prs
repos = pd.read_csv(path.reposCsvPath, header=0, sep=';', usecols=[0, 1, 2, 3])
 
def create_csv(result):
    prs =pd.DataFrame.from_records([result])
  
    if not (os.path.exists(path.prsCsvPath)):
        prs.to_csv(path.prsCsvPath, index=False, sep=';')
    else:
        prs.to_csv(path.prsCsvPath, index=False, sep=';',mode='a',header=False)
        
   
for index, repo in enumerate(repos.values.tolist()):  
        getPullRequestsQuery = getPullRequestsQuery.replace('nameWithOwner', repo[0])
        repoPrs = []
        endCursor = "null"

        result= run_query(getPullRequestsQuery)
                        
        if 'data' in result:
            for pr in result['data']['search']['nodes']:
                # verifica se pr foi fechado automaticamente (tem mais que uma hora entre criação e final)
                createdAt = datetime.datetime.strptime(
                    pr['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
                if pr['state'] == 'CLOSED':
                    closedAt = datetime.datetime.strptime(
                        pr['closedAt'], '%Y-%m-%dT%H:%M:%SZ')
                    diff = closedAt - createdAt
                    diffSeconds = diff.total_seconds()
                    hours = divmod(diffSeconds, 3600)[0]
                elif pr['state'] == 'MERGED':
                    mergedAt = datetime.datetime.strptime(
                        pr['mergedAt'], '%Y-%m-%dT%H:%M:%SZ')
                    diff = mergedAt - createdAt
                    diffSeconds = diff.total_seconds()
                    hours = divmod(diffSeconds, 3600)[0]
                        
                reviews = pr['reviews']['totalCount']
                pr['hours'] = hours   
                pr['reviews'] = pr['reviews']['totalCount']
                pr['comments'] = pr['comments']['totalCount']
                pr['participants'] = pr['participants']['totalCount'] 
                            
                if len(pr['bodyText']) > 0:
                    pr['bodyText'] = len(pr['bodyText'])
                else:
                    pr['bodyText'] = 0
                        
                create_csv(pr)
                        
            if (result['data']['search']['pageInfo']['endCursor'] is not None):
                getPullRequestsQuery = getPullRequestsQuery.replace(
                    endCursor, '"'+result['data']['search']['pageInfo']['endCursor']+'"')
                endCursor = '"' + \
                result['data']['search']['pageInfo']['endCursor']+'"'
            else:
                break
        else:
            print("Error na chamada da api do git hub")
            print(result)
            break
            
