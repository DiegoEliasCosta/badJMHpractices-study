import seaborn as sns
import matplotlib.pyplot as plt
import os
from utils import formatFileName


def comparissonPlot(df, anova_dir):
    # Formatting Dataframe to use Seaborn (melt)
    formatted_df = df[['Score_original', 'Score_fixed']]
    formatted_df = formatted_df.melt(value_vars=['Score_original', 'Score_fixed'], var_name='score')

    fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
    fig.suptitle(df.name)
    sns.boxplot(data=formatted_df, x='score', y='value', ax=axes[0])
    sns.violinplot(data=formatted_df, x='score', y='value', ax=axes[1])

    ylabel = df['Benchmark Mode'].iloc[0]
    axes[0].set_ylabel(ylabel)
    axes[1].set_ylabel(ylabel)

    # plt.show()
    name = formatFileName(df.name)

    fig_name = name + '.pdf'
    try:
        fig.savefig(os.path.join(anova_dir, fig_name))
    except:
        print('Error while trying to save the file %s' % fig_name)

    plt.clf()
    pass


def comparisonTable(df, summary_dir):



    pass