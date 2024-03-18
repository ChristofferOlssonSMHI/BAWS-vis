#!/usr/bin/env python3
"""
Created on 2021-10-18 18:42

@author: johannes
"""
import os
import pandas as pd
import numpy as np


fid = r'C:\Utveckling\BAWS-vis\bawsvis\examples\area_season_bloom_all.xlsx'

stats = None
for year in range(2002, 2023):
    df = pd.read_excel(
        fid,
        sheet_name=f'{year}',
    )
    if not stats:
        stats = {
            str(y): {
                a: {
                    'start': [],
                    'end': [],
                } for a in df['BASIN']
            } for y in range(2002, 2023)
        }

    for b in df['BASIN']:
        boolean = df['BASIN'] == b
        arr = df.loc[boolean, :].values
        idx = np.logical_or(arr == 2, arr == 3)[0]
        dates = df.columns[idx]
        if any(dates):
            stats[str(year)][b]['start'] = dates[0]
            stats[str(year)][b]['end'] = dates[-1]
        else:
            stats[str(year)][b]['start'] = np.nan
            stats[str(year)][b]['end'] = np.nan

mean_median = {
    'BASIN': [],
    'mean_start': [],
    'std_dev_start': [],
    'mean_end': [],
    'median_start': [],
    'median_end': [],
    'std_dev_end': [],
}

basins = df['BASIN'].to_list()
basins.append('All')
for b in basins:
    dummy_year = '2022{}'
    if b != 'All':
        start_values = [stats[y][b]['start'] for y in stats]
        start_values = pd.Series([pd.Timestamp(dummy_year.format(d[4:])) for d in start_values if not pd.isnull(d)])
        end_values = [stats[y][b]['end'] for y in stats]
        end_values = pd.Series([pd.Timestamp(dummy_year.format(d[4:])) for d in end_values if not pd.isnull(d)])
    else:
        start_values = []
        end_values = []
        for y in stats:
            start_values.append(min([pd.Timestamp(stats[y][b]['start'])
                                     for b in df['BASIN'] if type(stats[y][b]['start']) == str]))
            end_values.append(max([pd.Timestamp(stats[y][b]['end'])
                                   for b in df['BASIN'] if type(stats[y][b]['end']) == str]))
        start_values = pd.Series([ts.replace(year=2022) for ts in start_values if not pd.isnull(ts)])
        end_values = pd.Series([ts.replace(year=2022) for ts in end_values if not pd.isnull(ts)])

    std_start = start_values.std().components
    end_start = end_values.std().components
    mean_median['BASIN'].append(b)
    mean_median['mean_start'].append(start_values.mean())
    mean_median['mean_end'].append(end_values.mean())
    mean_median['median_start'].append(start_values.median())
    mean_median['median_end'].append(end_values.median())
    mean_median['std_dev_start'].append('{} days {} hours'.format(std_start.days, std_start.hours))
    mean_median['std_dev_end'].append('{} days {} hours'.format(end_start.days, end_start.hours))

final = pd.DataFrame(mean_median)
final.to_excel(
    'area_season_bloom_mean_median_2022_v3.xlsx',
    index=False
)
