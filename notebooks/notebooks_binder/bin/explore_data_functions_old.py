
'''
plots 2D PCA, with all paired of principal components

inputs :
    - X : peakTable with only variable columns, no metadata
    - dimensions (default=3) : number of principal components
'''
def PCA_paired(X, peakTable, dimensions=3):
    
    import plotly.express as px
    from sklearn.decomposition import PCA
    import cimcb_lite as cb
    
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
    
    import plotly.express as px
    from sklearn.decomposition import PCA
    import cimcb_lite as cb
    
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
    
    import numpy as np
    import pandas as pd
    
    from scipy.stats import shapiro

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
    
    import numpy as np
    import pandas as pd
    
    from scipy.stats import ttest_rel
    
    import time
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
    - alpha : threshold for shapiro test
return :
    - dataframe with boolean for normal distribution, applied test, statistic and pvalue for each variable (dataframe columns)
'''
def paired_ttest_or_Wilcoxon(peakTable_HILIC_POS, X, alpha=0.05):
    
    import numpy as np
    import pandas as pd
    
    from scipy.stats import shapiro   
    from scipy.stats import ttest_rel
    from scipy.stats import wilcoxon
    
    import time
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
        
        if shapiro(df_var['Diff'].values).pvalue > alpha:
            
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

    return infos



