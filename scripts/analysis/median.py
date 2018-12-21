from scipy import stats


def medianTest(df, alpha):

    original = df['Score_original']
    fixed = df['Score_fixed']

    stat, p, med, tbl = stats.median_test(original, fixed)

    if p < alpha:
        test = True
    else:
        test = False

    df['Median Test'] = test
    return df