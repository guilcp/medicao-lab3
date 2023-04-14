from src.queries import getRepositoriesQuery as y
from src.query_runner import run_query
import src.path as path
import pandas as pd


def fillRepoCsv():
    repositories = []
    endCursor = "null"
    getRepositoriesQuery = y

    error = 0
    while (len(repositories) < 200):
        
        
        result = run_query(getRepositoriesQuery)
        
        if 'data' in result:
            for repo in result['data']['search']['nodes']:
                # seleciona apenas repositorios com mais de 100 prs merged + closed
                if repo['closedPRs']['totalCount'] + repo['mergedPRs']['totalCount'] >= 100:
                    repo['closedPRs'] = repo['closedPRs']['totalCount']
                    repo['mergedPRs'] = repo['mergedPRs']['totalCount']
                    repo['totalPRs'] = repo['closedPRs'] + repo['mergedPRs']
                    repositories.append(repo)
                    
            if (result['data']['search']['pageInfo']['endCursor'] is not None):
                getRepositoriesQuery = getRepositoriesQuery.replace(endCursor, '"'+result['data']
                                  ['search']['pageInfo']['endCursor']+'"')
                endCursor = '"' + \
                    result['data']['search']['pageInfo']['endCursor']+'"'
        else:
            error += 1
            if (error > 5):
                print("Error na chamada da api do git hub")
                print(result)
                break
            else:
                continue

    df = pd.DataFrame(repositories)

    df.to_csv(path.reposCsvPath, index=False, sep=';')


# checa se csv de repositorios ja tem o numero suficiente, se nao tem preenche
if path.reposCsvPath.is_file():
    df = pd.read_csv(path.reposCsvName)
    if len(df.index) < (path.csvSize):
        fillRepoCsv()
else:
    fillRepoCsv()