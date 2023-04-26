
import pandas as pd
import src.path as path
import matplotlib.pyplot as plt
import seaborn as sns

prsResultsGraph = pd.read_csv(path.prsCsvPath, header= 0, sep=';')

# lmplot = sns.lmplot(x='changedFiles',y='reviews',data=prsResultsGraph,fit_reg=True) 
# lmplot.savefig('./graphs/lm_rq5.png') 
# print("RQ 5 - Coeficiente de correlação tamanho x reviews : ")
# print("pearson: ")
# print(prsResultsGraph['changedFiles'].corr(prsResultsGraph['reviews']))
# print("spearman: ")
# print(prsResultsGraph['changedFiles'].corr(prsResultsGraph['reviews'], method='spearman'))
# plt.clf()

# lmplot = sns.lmplot(x='hours',y='reviews',data=prsResultsGraph,fit_reg=True) 
# lmplot.savefig('./graphs/lm_rq6.png') 
# print("RQ 6 - Coeficiente de correlação tempo de análise x reviews : ")
# print("pearson: ")
# print(prsResultsGraph['hours'].corr(prsResultsGraph['reviews']))
# print("spearman: ")
# print(prsResultsGraph['hours'].corr(prsResultsGraph['reviews'], method='spearman'))
# plt.clf()

# lmplot = sns.lmplot(x='bodyText',y='reviews',data=prsResultsGraph,fit_reg=True) 
# lmplot.savefig('./graphs/lm_rq7.png') 
# print("RQ 7 - Coeficiente de correlação descrição x reviews : ")
# print("pearson: ")
# print(prsResultsGraph['bodyText'].corr(prsResultsGraph['reviews']))
# print("spearman: ")
# print(prsResultsGraph['bodyText'].corr(prsResultsGraph['reviews'], method='spearman'))
# plt.clf()

# interactions = prsResultsGraph[['participants', 'comments']].copy()
# interactions['cat'] = 'set1'

lmplot = sns.lmplot(x='participants',y='comments',hue='reviews',data=prsResultsGraph,fit_reg=True) 
lmplot.savefig('./graphs/lm_rq8.png') 
print("RQ 8 - Coeficiente de correlação interações x reviews : ")
print("pearson: ")
print(prsResultsGraph[['participants', 'comments', 'reviews']].corr())
print("spearman: ")
print(prsResultsGraph[['participants', 'comments', 'reviews']].corr(method='spearman'))
plt.clf()