import os

import h5py
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def draw():
    mi_array = np.array(
        [['8m', 'expert', 6.76],
        ['8m', 'medium', 6.52],
        ['8m', 'poor', 3.99],
        ['2s3z', 'expert', 6.86],
        ['2s3z', 'medium', 6.74],
        ['2s3z', 'poor', 6.00],
        ['5m_vs_6m', 'expert', 6.42],
        ['5m_vs_6m', 'medium', 5.63],
        ['5m_vs_6m', 'poor', 4.57],
        ['3s5z', 'expert', 6.34],
        ['3s5z', 'medium', 5.84],
        ['3s5z', 'poor', 4.32],
        ['27m_vs_30m', 'expert', 2.36],
        ['27m_vs_30m', 'medium', 1.78],
        ['27m_vs_30m', 'poor', 0.32],
        ['6h_vs_8z', 'expert', 6.16],
        ['6h_vs_8z', 'medium', 5.39],
        ['6h_vs_8z', 'poor', 4.00]]
    )

    mi_df = pd.DataFrame(mi_array ,columns=['Map Name', 'Quality', 'Mutual Information'])
    print(mi_df)

    mi_df = mi_df.explode('Mutual Information')
    mi_df['Mutual Information'] = mi_df['Mutual Information'].astype('float')

    ax = sns.barplot(x='Map Name', y='Mutual Information', hue='Quality', data=mi_df)
    plt.savefig('graphs/observability.pdf')
    plt.show()

draw()