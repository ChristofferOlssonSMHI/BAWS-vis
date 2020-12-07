# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-31 11:39

@author: a002028

"""
from bawsvis.session import Session
from bawsvis.data_handler import get_interpolated_data_table, get_interpolated_statistics_table, get_statistics
from bawsvis.interpolate import get_interpolated_df
from bawsvis.readers.dictionary import pandas_reader, json_reader
from bawsvis.utils import recursive_dict_update
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import dates

sns.set(style="darkgrid")
# sns.set(style="whitegrid")


def plot_one_season(stat_df):
    file = 'C:/Utveckling/BAWS-vis/bawsvis/export/stats_2020.json'
    data = pandas_reader(file)
    data.rename(columns={c: pd.Timestamp(str(c)) for c in data.columns}, inplace=True)
    df = get_interpolated_data_table(data)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5))

    ax1.fill_between(df.columns,
                    df.loc['weekly_bloom_area', :],
                    y2=df.loc['daily_bloom_area', :],
                    label='Weekly bloom',
                    lw=.1, alpha=.6,
                    color='grey')

    ax1.fill_between(df.columns,
                    df.loc['daily_bloom_area', :],
                    y2=df.loc['surface_area', :],
                    label='Daily bloom',
                    lw=.1, alpha=.8,
                    color='yellow')

    ax1.fill_between(df.columns,
                    df.loc['surface_area', :],
                    label='Surface accumulations',
                    lw=.1, alpha=.8,
                    color='orange')

    sns.lineplot(data=stat_df.loc['weekly_mean', :],
                 label='Mean weekly 2002-2020',
                 color='k',
                 ax=ax2)

    ax2.fill_between(stat_df.columns,
                    stat_df.loc['weekly_std_u', :],
                    y2=stat_df.loc['weekly_std_l', :],
                    label='St.Dev. weekly 2002-2020',
                    lw=.1, alpha=.6,
                    color='grey')

    ax2.xaxis.set_major_formatter(dates.DateFormatter("%d-%b"))
    ax2.set_xlim(stat_df.columns[0], stat_df.columns[-1])
    ax2.set_ylim(0, 200000)
    ax1.set_xlim(stat_df.columns[0], stat_df.columns[-1])
    ax1.set_ylim(0, 200000)

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper left')

    ax1.set_ylabel('km$^{2}$')
    ax2.set_ylabel('km$^{2}$')

    ax1.set_title('Cyanobacterial bloom 2020')

    plt.tight_layout()
    plt.savefig('diagram_2020.png', dpi=300)


if __name__ == "__main__":
    file_path = 'C:/Utveckling/BAWS-vis/bawsvis/export/stats_all.json'
    stat_data = get_statistics(file_path)
    df = pd.DataFrame(stat_data)
    idx = df['summer_dates'].values
    df.drop('summer_dates', axis=1, inplace=True)
    df.index = idx
    df = df.transpose()

    df = get_interpolated_statistics_table(df)

    plot_one_season(df)

    # fig, ax = plt.subplots(figsize=(10, 5))
    #
    # ax.fill_between(df.columns,
    #                 df.loc['weekly_std_u', :],
    #                 y2=df.loc['weekly_std_l', :],
    #                 label='Weekly bloom',
    #                 lw=.1, alpha=.2,
    #                 color='grey')

    # ax.fill_between(df.columns,
    #                 df.loc['daily_std_u', :],
    #                 y2=df.loc['daily_std_l', :],
    #                 label='Daily bloom',
    #                 lw=.1, alpha=.5,
    #                 color='yellow')

    # ax.legend(loc='upper left')
    # plt.ylabel('km$^{2}$')
    # plt.tight_layout()


