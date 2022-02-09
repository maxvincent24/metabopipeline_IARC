import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.decomposition import PCA

import scipy
from scipy.stats import shapiro   
from scipy.stats import ttest_rel
from scipy.stats import wilcoxon

import time

import seaborn as sns

import statsmodels.stats.multitest





'''
plots 2D PCA, with all paired of principal components

inputs :
    - X : peakTable with only variable columns, no metadata
    - dimensions (default=3) : number of principal components
'''
def PCA_paired(X, peakTable, dimensions=3):
    
    pca = PCA()
    components = pca.fit_transform(X)
    labels = {
        str(i): f"PC {i+1} ({var:.1f}%)"
        for i, var in enumerate(pca.explained_variance_ratio_ * 100)
    }

    fig = px.scatter_matrix(
        components,
        labels=labels,
        dimensions=range(dimensions),
        color=peakTable['Groups']
    )
    fig.update_traces(diagonal_visible=False)
    fig.show()
    

'''
plots 3D PCA

input :
    - X : peakTable with only variable columns, no metadata
''' 
def PCA_3D(X, peakTable):
    
    pca = PCA(n_components=3)
    components = pca.fit_transform(X)

    total_var = pca.explained_variance_ratio_.sum() * 100

    fig = px.scatter_3d(
        components, x=0, y=1, z=2, color=peakTable['Groups'],
        title=f'Total Explained Variance: {total_var:.2f}%',
        labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'},
        opacity=0.7
    )
    fig.show()

    
    
'''
Test of normality with Shapiro-Wilk test : scipy.stats.shapiro

performs shapiro test for each column in dataframe

input :
    - X : peakTable with only variable columns, no metadata
return :
    - dataframe with statistic and pvalue for each variable (dataframe columns)
'''   
def shapiro_test_df(X):

    infos = []

    for col in X.columns:

        curr_infos = []

        shapiro_test = shapiro(X[col][X[col].notna()])
        curr_infos.append(col)
        curr_infos.append(shapiro_test.statistic)
        curr_infos.append(shapiro_test.pvalue)


        infos.append(np.array(curr_infos))

    infos = pd.DataFrame(np.array(infos))
    infos.columns = ['Compounds', 'shapiro_score', 'pvalue']
    infos.index = infos['Compounds']
    infos = infos.drop(['Compounds'], axis=1)
    infos = infos.apply(pd.to_numeric, errors='coerce')

    return infos




'''
Paired t-test : scipy.stats.ttest_rel

For each column in dataframe, performs paired t-test between 'Incident' and 'Non-case' groups

input :
    - peakTable_HILIC_POS : whole peak table with variable and metadata
    - X : peakTable with only variable columns, no metadata
return :
    - dataframe with statistic and pvalue for each variable (dataframe columns)
'''  
def paired_ttest_df(peakTable_HILIC_POS, X):
    
    t0 = time.time()

    infos = []

    for variable in X.columns:

        curr_var = peakTable_HILIC_POS[['Groups', 'MatchCaseset', variable]]

        val_incident = []
        val_non_case = []
        case_id = []

        for elt in np.unique(curr_var['MatchCaseset']):

            curr_case = curr_var[curr_var['MatchCaseset'] == elt]

            case_id.append(elt)
            val_incident.append(curr_case[curr_case['Groups'] == 'Incident'][variable].values[0])
            val_non_case.append(curr_case[curr_case['Groups'] == 'Non-case'][variable].values[0])

        df_var = pd.concat([pd.Series(case_id), pd.Series(val_incident), pd.Series(val_non_case)], axis=1)
        df_var.columns = ['MatchCaseset', 'Incident', 'Non-case']


        curr_ttest = ttest_rel(df_var['Incident'].values, df_var['Non-case'].values, nan_policy='omit')
        curr_ttest_values = [variable, curr_ttest.statistic, curr_ttest.pvalue]

        infos.append(curr_ttest_values)


    infos = pd.DataFrame(np.array(infos))
    infos.columns = ['Variable', 'statistic', 'pvalue']
    infos.index = infos['Variable']
    infos = infos.drop(['Variable'], axis=1)
    infos = infos.apply(pd.to_numeric, errors='coerce')
    
    print('Time to compute : {0}'.format(time.strftime("%H:%M:%S", time.gmtime(time.time() - t0))))

    return infos




'''
Paired t-test : scipy.stats.ttest_rel
Wilcoxon test : scipy.stats.wilcoxon

For each column in dataframe :
- test with shapiro test if differences between paires are normally distributed
- if yes, performs paired t-test between 'Incident' and 'Non-case' groups
- if no, performs wilcoxon test between 'Incident' and 'Non-case' groups

input :
    - peakTable_HILIC_POS : whole peak table with variable and metadata
    - X : peakTable with only variable columns, no metadata
    - alpha_shapiro : threshold for shapiro test
return :
    - dataframe with boolean for normal distribution, applied test, statistic and pvalue for each variable (dataframe columns)
'''
def paired_test_t_or_Wilcoxon(peakTable_HILIC_POS, X, alpha_shapiro=0.05):
    
    t0 = time.time()

    infos = []
    
    count = 0

    for variable in X.columns:

        curr_var = peakTable_HILIC_POS[['Groups', 'MatchCaseset', variable]]

        val_incident = []
        val_non_case = []
        case_id = []
        val_diff = []

        for elt in np.unique(curr_var['MatchCaseset']):

            curr_case = curr_var[curr_var['MatchCaseset'] == elt]

            case_id.append(elt)
            val_incident.append(curr_case[curr_case['Groups'] == 'Incident'][variable].values[0])
            val_non_case.append(curr_case[curr_case['Groups'] == 'Non-case'][variable].values[0])
            val_diff.append((curr_case[curr_case['Groups'] == 'Incident'][variable].values[0]) - (curr_case[curr_case['Groups'] == 'Non-case'][variable].values[0]))
            
        df_var = pd.concat([pd.Series(case_id), pd.Series(val_incident), pd.Series(val_non_case), pd.Series(val_diff)], axis=1)
        df_var.columns = ['MatchCaseset', 'Incident', 'Non-case', 'Diff']
        
        if scipy.stats.shapiro(df_var['Diff'].values).pvalue > alpha_shapiro:
            
            # difference between paires is normally distributed so paired t-test (parametric)
            normally_distibuted = True
            test_applied = 'Paired t-test'
            
            curr_ttest = ttest_rel(df_var['Incident'].values, df_var['Non-case'].values, nan_policy='omit')
            curr_ttest_values = [variable, normally_distibuted, test_applied, curr_ttest.statistic, curr_ttest.pvalue]
            
        else:
            
            # difference between paires isn't normally distributed so Wilcoxon test (non-parametric)
            normally_distibuted = False
            test_applied = 'Wilcoxon'
            
            curr_ttest = wilcoxon(df_var['Diff'].values)
            curr_ttest_values = [variable, normally_distibuted, test_applied, curr_ttest.statistic, curr_ttest.pvalue]
            
        infos.append(curr_ttest_values)


    infos = pd.DataFrame(np.array(infos))
    infos.columns = ['Variable', 'NormallyDistributed', 'TestApplied', 'statistic', 'pvalue']
    infos.index = infos['Variable']
    infos = infos.drop(['Variable'], axis=1)
    infos['statistic'] = infos['statistic'].apply(pd.to_numeric, errors='coerce')
    infos['pvalue'] = infos['pvalue'].apply(pd.to_numeric, errors='coerce')
    
    
    print('Time to compute : {0}'.format(time.strftime("%H:%M:%S", time.gmtime(time.time() - t0))))

    return infos, df_var




'''
Correct the list of pvalues using the inputed correction type
input :
    - df : dataframe output of function paired_test_t_or_Wilcoxon
    - correction: name of the multiple testing correction to use (values: Bf, H-BF (by default), Benj-Hoch)
    - alpha : thresold of significance level
return :
    - input df with some columns added with the corrected p-values
'''
def pvalue_correction(df, correction = 'Bonferroni', alpha = 0.05):

    ech_size = df.shape[0]
    updated = df.copy()
    updated['alpha'] = alpha
    updated['H0rejected'] = updated['pvalue'] < alpha
    
    if correction == 'Bonferroni':
        
        updated['alphaCorrected'] = alpha / ech_size
        updated['H0rejectedCorrected'] = updated['pvalue'] < updated['alphaCorrected']
    
    elif correction == 'Holm-Bonferroni':
        
        updated_sorted = updated.sort_values('pvalue', ascending=True)
        updated_sorted['Rank'] = np.arange(ech_size, 0, -1)
        updated_sorted['alphaCorrected'] = updated['alpha'] / updated_sorted['Rank']
        updated_sorted['H0rejectedCorrected'] = updated_sorted['pvalue'] < updated_sorted['alphaCorrected']
    
        updated = updated_sorted.reindex(updated.index)
        
    elif correction == 'Benjamini-Hochberg':
        
        updated_sorted = updated.sort_values('pvalue', ascending=True)
        updated_sorted['Rank'] = np.arange(1, ech_size + 1)
        updated_sorted['alphaCorrected'] = updated_sorted['Rank'] / ech_size * alpha
        updated_sorted['H0rejectedCorrected'] = updated_sorted['pvalue'] < updated_sorted['alphaCorrected']
    
        updated = updated_sorted.reindex(updated.index)
    
    elif correction == 'FDR':
        
        Rejects, AdjustedPValues = statsmodels.stats.multitest.fdrcorrection(df['pvalue'], alpha=alpha, method='indep', is_sorted=False)
        updated = pd.concat([updated, pd.DataFrame({'pvalueAdjusted': AdjustedPValues, 'H0rejectedAdjusted': Rejects}, index=df.index)], axis=1)
        
    else:
        print("Correction not recognized")
        updated = df
        
    return updated





'''
Plot the p-values for each variable
input :
    - df : output of function pvalue_correction
'''
def plot_pvalue(df):
    
    df = df.sort_values(by='pvalue')

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(30,6))
    fig.suptitle('p-value for each feature', fontsize=20, y=1.05)    
    
    # whole plot
    ax1.plot(df['pvalue'].values, color='b', linewidth=2, label='p-value')
    ax1.plot(df['alpha'].values, color='r', linewidth=1, label='alpha')
    ax1.plot(df['alphaCorrected'].values, color='g', linewidth=1, label='alphaCorrected')
    ax1.set_xlabel('N° of the compound', fontsize=12)
    ax1.set_ylabel('p-value', fontsize=12)
    ax1.legend(loc='upper left', prop={'size': 12})
    ax1.set_title('whole plot', fontsize=15)
    ax1.grid(linestyle='--', linewidth=1)
    
    
    # zoom on features under alpha
    subset1 = df.loc[:df[df['H0rejected'] == False].index[2], :]
    
    ax2.plot(subset1['pvalue'].values, color='b', linewidth=2, label='p-value')
    ax2.plot(subset1['alpha'].values, color='r', linewidth=2, label='alpha')
    ax2.plot(subset1['alphaCorrected'].values, color='g', linewidth=2, label='alphaCorrected')
    ax2.set_xlabel('N° of the compound', fontsize=12)
    ax2.set_ylabel('p-value', fontsize=12)
    ax2.legend(loc='upper left', prop={'size': 12})
    ax2.set_title('zoom on features under alpha', fontsize=15)
    ax2.grid(linestyle='--', linewidth=1)
    
    
    # zoom on features under alphaCorrected
    subset2 = df.loc[:df[df['H0rejectedCorrected'] == False].index[0], :]
    
    ax3.plot(subset2['pvalue'].values, color='b', linewidth=2, label='p-value')
    ax3.plot(subset2['alphaCorrected'].values, color='g', linewidth=2, label='alphaCorrected')
    ax3.set_xlabel('N° of the compound', fontsize=12)
    ax3.set_ylabel('p-value', fontsize=12)
    ax3.ticklabel_format(useOffset=False, style='plain')
    ax3.legend(loc='upper left', prop={'size': 12})
    ax3.set_title('zoom on features under alphaCorrected', fontsize=15)
    ax3.grid(linestyle='--', linewidth=1)
    
    

    
    
'''
Plot the relative log abundance for each variable and each sample
input :
    - X : peakTable with only variable columns, no metadata
'''
def plot_relative_log_abundance(X):
    
    plt.figure(figsize=(20, 15))

    plt.suptitle('Relative log abundance', fontsize=20)

    plt.subplot(2, 1, 1)
    if X.shape[1] > 100 :
        X2 = X.iloc[:,:100]
        rel_log_abundance_metabolite = np.log(X2) - np.log(X2).median()
    else :
        rel_log_abundance_metabolite = np.log(X) - np.log(X).median()
    boxplot = sns.boxplot(data=rel_log_abundance_metabolite)
    boxplot.set_xticklabels(boxplot.get_xticklabels(), rotation=90)
    plt.title('Based on metabolites', fontsize=16)

    plt.subplot(2, 1, 2)
    rel_log_abundance_sample = np.log(X) - np.array(np.log(X).median(axis=1)).reshape(X.median(axis=1).shape[0], 1)
    boxplot = sns.boxplot(data=rel_log_abundance_sample.transpose())
    boxplot.set_xticklabels(boxplot.get_xticklabels(), rotation=90)
    plt.title('Based on samples', fontsize=16)

    plt.subplots_adjust(hspace=0.4)
    plt.show()

    None
    
    
    
    
    
    
    
'''
Plot the histogram of pvalues
input :
    - df : dataframe output of function paired_test_t_or_Wilcoxon
    - alpha : chosen threshold for alpha
'''  
def plot_hist_pvalue(df, alpha=0.05, plot_corrected=False):
    
    if plot_corrected:
        
        fig, ax = plt.subplots(1, 2, figsize=(24, 8))

        freq, bins, _ = ax[0].hist(df['pvalue'], np.arange(0, 1, alpha), color='coral', edgecolor='black', alpha=0.5, label=f'pvalue > {alpha}')
        count, _ = np.histogram(df['pvalue'], bins)
        for x,y,num in zip(bins, freq, count):
            if num != 0:
                ax[0].text(x+alpha/3, y+1, num, fontsize=10) # x,y,str
        ax[0].set_xticks(np.arange(0, 1, 0.05))
        ax[0].set_title('Histogram of p-values', fontsize=20)

        # add green on bin with pvalue < alpha
        hist2 = ax[0].hist(df['pvalue'][df['pvalue'] < alpha], np.arange(0, 1, alpha), color='mediumseagreen', edgecolor='black', alpha=1, label=f'pvalue < {alpha}')

        ax[0].legend(loc='upper right', prop={"size":15})   
        
        
        
        freq, bins, _ = ax[1].hist(df['pvalueAdjusted'], np.arange(0, 1, alpha), color='coral', edgecolor='black', alpha=0.5, label=f'pvalueAdjusted > {alpha}')
        count, _ = np.histogram(df['pvalueAdjusted'], bins)
        for x,y,num in zip(bins, freq, count):
            if num != 0:
                ax[1].text(x+alpha/3, y+1, num, fontsize=10) # x,y,str
        ax[1].set_xticks(np.arange(0, 1, 0.05))
        ax[1].set_title('Histogram of corrected p-values', fontsize=20)

        # add green on bin with pvalue < alpha
        hist2 = ax[1].hist(df['pvalueAdjusted'][df['pvalueAdjusted'] < alpha], np.arange(0, 1, alpha), color='mediumseagreen', edgecolor='black', alpha=1, label=f'pvalueAdjusted < {alpha}')

        ax[1].legend(loc='upper right', prop={"size":15})  

        
    else:
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))

        freq, bins, _ = ax.hist(df['pvalue'], np.arange(0, 1, alpha), color='coral', edgecolor='black', alpha=0.5, label=f'pvalue > {alpha}')
        count, _ = np.histogram(df['pvalue'], bins)
        for x,y,num in zip(bins, freq, count):
            if num != 0:
                ax.text(x+alpha/3, y+1, num, fontsize=10) # x,y,str
        ax.set_xticks(np.arange(0, 1, 0.05))
        plt.title('Histogram of p-values', fontsize=20)

        # add green on bin with pvalue < alpha
        hist2 = ax.hist(df['pvalue'][df['pvalue'] < alpha], np.arange(0, 1, alpha), color='mediumseagreen', edgecolor='black', alpha=1, label=f'pvalue < {alpha}')

        plt.legend(loc='upper right', prop={"size":15})       
        

    plt.show()