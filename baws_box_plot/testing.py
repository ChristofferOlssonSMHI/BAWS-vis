#!/usr/bin/env python3
"""
Created on 2021-10-15 15:41

@author: johannes
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import seaborn as sns
sns.set(style="whitegrid")


def change_width(ax, new_value):
    for patch in ax.patches:
        current_width = patch.get_height()
        diff = current_width - new_value
        patch.set_height(new_value)
        patch.set_y(patch.get_y() + diff * .5)


fig, ax = plt.subplots(nrows=1)

data = {
    'ts_start': [
        '2021-07-01',
        '2021-07-01',
        '2021-07-01',
        '2021-06-25',
    ],
    'ts_end': [
        '2021-07-30',
        '2021-07-10',
        '2021-08-30',
        '2021-07-05'
    ],
    'area': [
        'Southern',
        'Central',
        'Northern',
        'Bothnia',
    ]
}
df = pd.DataFrame(data)
data2 = {
    'ts_start': [
        '2021-08-05',
        '2021-08-15',
        np.nan,
        np.nan,
    ],
    'ts_end': [
        '2021-08-30',
        '2021-08-20',
        np.nan,
        np.nan,
    ],
    'area': [
        'Central',
        'Northern',
        'Bothnia',
        'Southern',
    ]
}
df2 = pd.DataFrame(data2)
df['ts_start'] = df['ts_start'].apply(lambda x: mdates.datestr2num(x))
df['ts_end'] = df['ts_end'].apply(lambda x: mdates.datestr2num(x))
df2['ts_start'] = [np.nan if pd.isnull(x) else mdates.datestr2num(x) for x in df2['ts_start']]
df2['ts_end'] = [np.nan if pd.isnull(x) else mdates.datestr2num(x) for x in df2['ts_end']]

ax.use_sticky_edges = False
fig.autofmt_xdate()

b = sns.barplot(
    y=df['area'],
    x=df['ts_end'] - df['ts_start'],
    left=df['ts_start'],
    ec='k',
    color='white',
    ax=ax
)

a = sns.barplot(
    y=df2['area'],
    x=df2['ts_end'] - df2['ts_start'],
    left=df2['ts_start'],
    ec='k',
    color='white',
    ax=ax
)

change_width(ax, .5)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))

sns.despine(offset=5, bottom=True, left=True)
plt.tight_layout()
plt.show()


# tips = sns.load_dataset('tips')
# fig, ax = plt.subplots()
#
# day_min_max = tips[['day', 'total_bill']].groupby('day').agg(['min', 'max', 'median'])
# day_min_max.columns = day_min_max.columns.droplevel(0)
# day_min_max = day_min_max.reset_index()
#
# """
# day_min_max:
#     day   min    max  median
# 0  Thur  7.51  43.11   16.20
# 1   Fri  5.75  40.17   15.38
# 2   Sat  3.07  50.81   18.24
# 3   Sun  7.25  48.17   19.63
# """
#
# ax.use_sticky_edges = False
# sns.barplot(
#     y=day_min_max['day'],
#     x=day_min_max['max'] - day_min_max['min'],
#     left=day_min_max['min'],
#     color='white',
#     ec='k',
#     ax=ax
# )
#
#
# change_width(ax, .5)
#
# plt.tight_layout()
# plt.show()
