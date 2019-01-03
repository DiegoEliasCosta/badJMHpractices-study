from scipy import stats



def anovaCheck(df, alpha):
    original = df['Score_original']
    fixed = df['Score_fixed']
    f, p = stats.f_oneway(original, fixed)
    if p < alpha:
        significant = True
    else:
        significant = False
    df['ANOVA'] = significant
    return df


