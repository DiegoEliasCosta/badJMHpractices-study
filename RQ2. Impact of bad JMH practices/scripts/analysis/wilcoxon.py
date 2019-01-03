from scipy import stats


def wilcoxonTest(df, alpha):

    print(df.name)

    original = df['Score_original']
    print('Original: %d' % len(original))
    fixed = df['Score_fixed']
    print('Fixed: %d' % len(fixed))

    T, p = stats.wilcoxon(original, fixed)

    if p < alpha:
        test = True
    else:
        test = False

    df['Wilcoxon Test'] = test
    return df