import pandas as pd
import src.path as path
import os

def create_csv(result):
    prs =pd.DataFrame.from_records([result])
  
    if not (os.path.exists(path.prsFilterCsvPath)):
        prs.to_csv(path.prsFilterCsvPath, index=False, sep=';')
    else:
        prs.to_csv(path.prsFilterCsvPath, index=False, sep=';',mode='a',header=False)

def pr_filter(csv):
    filteredPrs = {}
    
    for repo in csv.to_dict(orient='records'):
        if repo['hours'] >= 1 and repo['reviews'] >= 1:
            filteredPrs['repository'] = repo['repository']
            filteredPrs['state'] = repo['state']
            filteredPrs['createdAt'] = repo['createdAt']
            if(repo['state'] == 'MERGED'):
                filteredPrs['mergedAt'] = repo['mergedAt']
            else:
                filteredPrs['mergedAt'] = 'NaN'
            if(repo['state'] == 'CLOSED'):
                filteredPrs['closedAt'] = repo['closedAt']
            else:
                filteredPrs['closedAt'] = 'NaN'
            filteredPrs['reviews'] = repo['reviews']
            filteredPrs['participants'] = repo['participants']
            filteredPrs['bodyText'] = repo['bodyText']
            filteredPrs['changedFiles'] = repo['changedFiles']
            filteredPrs['comments'] = repo['comments']
            filteredPrs['additions'] = repo['additions']
            filteredPrs['deletions'] = repo['deletions']
            filteredPrs['hours'] = repo['hours']
            
            create_csv(filteredPrs)

# le do csv de repositorios e itera sobre eles para consultar os prs
prs = pd.read_csv(path.prsCsvPath, header=0, sep=';')

pr_filter(prs)