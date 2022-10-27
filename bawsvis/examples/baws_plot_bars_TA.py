#!/usr/bin/env python3
# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-11-08 12:22

@author: johannes
"""
import numpy as np
import pandas as pd
from scipy import interpolate
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import dates

sns.set(style="ticks", palette="pastel")
# sns.set(style="darkgrid")
# sns.set(style="whitegrid")


def change_width(ax, new_value):
    for patch in ax.patches:
        current_width = patch.get_width()
        diff = current_width - new_value
        patch.set_width(new_value)
        patch.set_x(patch.get_x() + diff * .5)


if __name__ == "__main__":
    df = pd.read_excel(
        r'C:\Temp\baws_reanalys\annual_stats_norm.xlsx',
        sheet_name='data',
    )

    label_mapper = {
        'total_area': 'Total area (km$^{2}$)',
        'duration': 'Varaktighet (dagar)',
        'extent': 'Utsträckning (km$^{2}$)',
        'intensity': 'Intensitet (km$^{2}$-days)',
    }
    # fig, ax = plt.subplots(1, 1, figsize=(8, 3))
    fig, axes = plt.subplots(4, 1, figsize=(8, 8), sharex=True)
    for ax, data_key, note in zip(axes, ('total_area', 'duration', 'extent', 'intensity'),
                                  ('a', 'b', 'c', 'd')):
        sns.barplot(x=df['year'], y=df[data_key],
                    color='gray',
                    ax=ax)
        change_width(ax, .5)
        sns.despine(offset=5, ax=ax, fig=fig)
        if data_key != 'duration':
            ax.ticklabel_format(axis='y', style='sci', scilimits=(1, 2), useMathText=True)
        ax.set_ylabel(label_mapper.get(data_key))
        ax.set_xlabel('')

        y_text_pos = ax.get_ylim()[1] - (ax.get_ylim()[1] - ax.get_ylim()[0]) / 9.
        ax.text(ax.get_xlim()[-1], y_text_pos, note)

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig('total_area.png', dpi=600)
