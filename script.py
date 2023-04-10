
import requests
import pandas as pd
from pathlib import Path
import datetime

# colocar token aqui
token = "KM4r0WcRDdbDewRvZ71dMEjG0kLky543xsx6"

headers = {"Authorization": "bearer ghp_"+token}

csvSize = 500
reposCsvName = 'repositories.csv'
reposCsvPath = Path('./'+reposCsvName)

prsCsvName = 'pullRequests.csv'
prsCsvPath = Path('./'+prsCsvName)


def fillRepoCsv():
    repositories = []
    query = """
    {
        search(
            query: "stars:>100"
            type: REPOSITORY
            first: 20
            after: null
        ) {
            pageInfo {
            endCursor
            startCursor
            }
            nodes {
                ... on Repository {
                    nameWithOwner
                    closedPRs: pullRequests(states: CLOSED, first: 1) {
                        totalCount
                    }
                    mergedPRs: pullRequests(states: MERGED, first: 1) {
                        totalCount
                    }
                }
            }
        }
    }
    """

    endCursor = "null"

    error = 0
    while (len(repositories) < 500):
        request = requests.post('https://api.github.com/graphql',
                                json={'query': query}, headers=headers)
        result = request.json()
        if 'data' in result:
            for repo in result['data']['search']['nodes']:
                # seleciona apenas repositorios com mais de 100 prs merged + closed
                if repo['closedPRs']['totalCount'] + repo['mergedPRs']['totalCount'] >= 100:
                    repo['closedPRs'] = repo['closedPRs']['totalCount']
                    repo['mergedPRs'] = repo['mergedPRs']['totalCount']
                    repo['totalPRs'] = repo['closedPRs'] + repo['mergedPRs']
                    repositories.append(repo)
            query = query.replace(endCursor, '"'+result['data']
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

    df.to_csv(reposCsvName, index=False, sep=';')


# checa se csv de repositorios ja tem o numero suficiente, se nao tem preenche
if reposCsvPath.is_file():
    df = pd.read_csv(reposCsvName)
    if len(df.index) < (csvSize):
        fillRepoCsv()
else:
    fillRepoCsv()

# le do csv de repositorios e itera sobre eles para consultar os prs
repos = pd.read_csv(reposCsvPath, header=0, sep=';', usecols=[0, 1, 2, 3])

if prsCsvPath.is_file():
    prsResults = pd.read_csv(prsCsvPath, header=0, sep=';')
else:
    prsResults = pd.DataFrame()


for index, repo in enumerate(repos.values.tolist()):
    if len(prsResults) > 0 and prsResults['repository'].tolist().count(repo[0]) >= repo[3]:
        continue
    else:
        query = """
            {
                search(
                    query: \"type:pr repo:nameWithOwner state:closed state:merged\"
                    type: ISSUE
                    first: 30
                    after: null
                ) {
                    pageInfo {
                        endCursor
                        startCursor
                    }
                    nodes {
                        ... on PullRequest {
                            repository {
                                owner {
                                    login
                                }
                                name
                            }
                            title
                            state
                            createdAt
                            mergedAt
                            closedAt
                        }
                    }
                }
            }
        """
        query = query.replace('nameWithOwner', repo[0])
        prs = []
        repoPrs = []
        endCursor = "null"
        error = 0
        if len(prsResults) > 0:
            prsAlreadyConsulted = prsResults['repository'].tolist().count(
                repo[0])
        else:
            prsAlreadyConsulted = 0
        while (len(repoPrs) < (repo[3] - prsAlreadyConsulted)):
            request = requests.post('https://api.github.com/graphql',
                                    json={'query': query}, headers=headers)
            result = request.json()
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
                    if hours >= 1:
                        pr['repository'] = pr['repository']['owner']['login'] + \
                            pr['repository']['name']
                        repoPrs.append(pr)
                query = query.replace(
                    endCursor, '"'+result['data']['search']['pageInfo']['endCursor']+'"')
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
        prsResults = pd.concat(
            [prsResults, pd.DataFrame.from_records([repoPrs])])
        prsResults.to_csv(prsCsvName, index=False, sep=';')
