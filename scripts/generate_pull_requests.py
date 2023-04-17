
import json
import pandas as pd
import datetime
import os
from src.query_runner import run_query
from src.queries import getPullRequestsQuery
import src.path as path


# le do csv de repositorios e itera sobre eles para consultar os prs
repos = pd.read_csv(path.reposCsvPath, header=0, sep=';', usecols=[0, 1, 2, 3])


def create_csv(result):
    prs = pd.DataFrame.from_records(result)

    if not (os.path.exists(path.prsCsvPath)):
        prs.to_csv(path.prsCsvPath, index=False, sep=';')
    else:
        prs.to_csv(path.prsCsvPath, index=False,
                   sep=';', mode='a', header=False)


if path.prsCsvPath.is_file():
    prsResults = pd.read_csv(path.prsCsvPath, header=0, sep=';')
else:
    prsResults = pd.DataFrame()

for index, repo in enumerate(repos.values.tolist()):
    endCursor = "null"
    if len(prsResults) > 0 :
        lastRegister = prsResults.values.tolist()[len(prsResults) - 1]
        lastRepo = json.loads(lastRegister[0].replace("'", "\"")) 
        login, name = repo[0].split("/")
        ex = {
            'owner': {
                'login': login
            },
            'name': name
        }
        repoPrs = prsResults.loc[prsResults['repository'] == str(ex)]
        if len(repoPrs) == 0:
            endCursor = "null"
        elif repo[0] != lastRepo['owner']['login']+"/"+lastRepo['name']:
            continue
        else:
            endCursor = '"'+lastRegister[16]+'"'

    owner, name = repo[0].split('/')
    prsRepoQuery = getPullRequestsQuery.replace(
        '{owner}', owner)
    prsRepoQuery = prsRepoQuery.replace(
        '{name}', name)
    prsRepoQuery = prsRepoQuery.replace(
        'null', endCursor)
    
    while True:
        print(endCursor)
        requestRepos = []
        result = run_query(prsRepoQuery)

        if 'data' in result:
            for pr in result['data']['repository']['pullRequests']['nodes']:
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
                pr['endCursor'] = result['data']['repository']['pullRequests']['pageInfo']['endCursor']

                if len(pr['bodyText']) > 0:
                    pr['bodyText'] = len(pr['bodyText'])
                else:
                    pr['bodyText'] = 0

                requestRepos.append(pr)
                # prsResults = prsResults.append(pr, ignore_index=True)

            # prsResults.concat(repoPrs)
            create_csv(requestRepos)
            if (result['data']['repository']['pullRequests']['pageInfo']['endCursor'] is not None):
                prsRepoQuery = prsRepoQuery.replace(
                    endCursor, '"'+result['data']['repository']['pullRequests']['pageInfo']['endCursor']+'"')
                endCursor = '"' + \
                    result['data']['repository']['pullRequests']['pageInfo']['endCursor']+'"'
            else:
                break
        else:
            print("Error na chamada da api do git hub")
            print(result)
            break

    # create_csv(repoPrs)
