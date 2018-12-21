from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import os
from utils import formatFileName


def checkNormality(df, alpha):
    def normalityTest(x):

        if len(x) < 8:
            return 'Not enough samples'

        k2, p = stats.normaltest(x)
        if p < alpha:
            return False
        else:
            return True

    df['Normality_original'] = normalityTest(df['Score_original'])
    df['Normality_fixed'] = normalityTest(df['Score_fixed'])

    return df


def plotNormalityComparison(df, normality_dir):
    # print('%s %s' % (df['Normality_original'].iloc[0], df['Normality_fixed'].iloc[0]))
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    original = df['Score_original']
    fixed = df['Score_fixed']

    fig.suptitle(df.name)

    sns.distplot(original, label='original', ax=axes[0])
    sns.distplot(fixed, label='fixed', ax=axes[1])

    # axes[0].set_ylabel(ylabel)
    axes[0].set_title('Normaly Distributed = %s' % df['Normality_original'].iloc[0])

    # axes[1].set_ylabel(ylabel)
    axes[1].set_title('Normaly Distributed = %s' % df['Normality_fixed'].iloc[0])

    # plt.show()
    name = formatFileName(df.name)
    fig_name = name + '.pdf'
    try:
        fig.savefig(os.path.join(normality_dir, fig_name))
    except:
        print('Error while trying to save the file %s' % fig_name)

    plt.clf()
    pass
