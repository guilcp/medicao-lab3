
import pandas as pd
import src.path as path
import matplotlib.pyplot as plt
import seaborn as sns

prsResultsGraph = pd.read_csv(path.prsCsvPath, header=0, sep=';')

prsResultsGraph['size'] = prsResultsGraph['additions'] + \
    prsResultsGraph['deletions']

# lmplot = sns.lmplot(x='changedFiles',y='size',hue='state',data=prsResultsGraph,fit_reg=True)
# lmplot.savefig('./graphs/lm_rq1.png')
# plt.clf()
print("RQ 1 - Coeficiente de correlação tamanho x feedback final : ")
print("pearson: ")
print(prsResultsGraph['changedFiles'].corr(prsResultsGraph['size']))
print("spearman: ")
print(prsResultsGraph['changedFiles'].corr(
    prsResultsGraph['size'], method='spearman'))


# boxplot = sns.boxplot(x='hours',y='state',data=prsResultsGraph,order=['CLOSED', 'MERGED'])
# plt.savefig('./graphs/lm_rq2.png')
# plt.clf()
print("RQ 2 - Coeficiente de correlação tempo x feedback final : ")
print("pearson: ")
# print(prsResultsGraph['hours'].corr(prsResultsGraph['state']))
print("spearman: ")
# print(prsResultsGraph['hours'].corr(prsResultsGraph['state'], method='spearman'))


# boxplot = sns.boxplot(x='bodyText',y='state',data=prsResultsGraph,order=['CLOSED', 'MERGED'])
# plt.savefig('./graphs/lm_rq3.png')
# plt.clf()
print("RQ 3 - Coeficiente de correlação descrição x feedback final : ")
print("pearson: ")
# print(prsResultsGraph['bodyText'].corr(prsResultsGraph['state']))
print("spearman: ")
# print(prsResultsGraph['bodyText'].corr(prsResultsGraph['state'], method='spearman'))


# lmplot = sns.lmplot(x='participants',y='comments',hue='state',data=prsResultsGraph,fit_reg=True)
# lmplot.savefig('./graphs/lm_rq4.png')
# plt.clf()
print("RQ 4 - Coeficiente de correlação interações x feedback final : ")
print("pearson: ")
print(prsResultsGraph['participants'].corr(prsResultsGraph['comments']))
print("spearman: ")
print(prsResultsGraph['participants'].corr(
    prsResultsGraph['comments'], method='spearman'))


# pplot = sns.pairplot(vars=['changedFiles', 'size', 'reviews'],
#  data=prsResultsGraph, kind='reg', x_vars=['reviews'], y_vars=['changedFiles', 'size'])
# plt.savefig('./graphs/lm_rq5.png')
# lmplot = sns.lmplot(x='changedFiles',y='reviews',data=prsResultsGraph,fit_reg=True)
# lmplot.savefig('./graphs/lm_rq5_p1.png')
# plt.clf()
# lmplot = sns.lmplot(x='size',y='reviews',data=prsResultsGraph,fit_reg=True)
# lmplot.savefig('./graphs/lm_rq5_p2.png')
# plt.clf()
print("RQ 5 - Coeficiente de correlação tamanho x reviews : ")
print("pearson: ")
print(prsResultsGraph[['changedFiles', 'size', 'reviews']].corr())
print("spearman: ")
print(prsResultsGraph[['changedFiles', 'size','reviews']].corr(method='spearman'))


# lmplot = sns.lmplot(x='hours',y='reviews',data=prsResultsGraph,fit_reg=True)
# lmplot.savefig('./graphs/lm_rq6.png')
# plt.clf()
print("RQ 6 - Coeficiente de correlação tempo de análise x reviews : ")
print("pearson: ")
print(prsResultsGraph['hours'].corr(prsResultsGraph['reviews']))
print("spearman: ")
print(prsResultsGraph['hours'].corr(
    prsResultsGraph['reviews'], method='spearman'))


# lmplot = sns.lmplot(x='bodyText',y='reviews',data=prsResultsGraph,fit_reg=True)
# lmplot.savefig('./graphs/lm_rq7.png')
# plt.clf()
print("RQ 7 - Coeficiente de correlação descrição x reviews : ")
print("pearson: ")
print(prsResultsGraph['bodyText'].corr(prsResultsGraph['reviews']))
print("spearman: ")
print(prsResultsGraph['bodyText'].corr(
    prsResultsGraph['reviews'], method='spearman'))


# interactions = prsResultsGraph[['participants', 'comments']].copy()
# interactions['cat'] = 'set1'

# lmplot = sns.lmplot(x='participants',y='reviews',data=prsResultsGraph,fit_reg=True)
# lmplot.savefig('./graphs/lm_rq8_p1.png')
# plt.clf()
# lmplot = sns.lmplot(x='comments',y='reviews',data=prsResultsGraph,fit_reg=True)
# lmplot.savefig('./graphs/lm_rq8_p2.png')
# plt.clf()
print("RQ 8 - Coeficiente de correlação interações x reviews : ")
print("pearson: ")
print(prsResultsGraph[['participants', 'comments', 'reviews']].corr())
print("spearman: ")
print(prsResultsGraph[['participants', 'comments', 'reviews']].corr(
    method='spearman'))
