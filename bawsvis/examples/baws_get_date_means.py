#!/usr/bin/env python3
# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-11-17 15:14

@author: johannes
"""
from bawsvis.session import Session
from bawsvis.readers.dictionary import json_reader
import os
import pandas as pd
import numpy as np


if __name__ == "__main__":
    s = Session()

    stat = json_reader(os.path.join(s.setting.export_directory, 'stats_all.json'))
    stat = {pd.Timestamp(d): item for d, item in stat.items()}

    dummy_year = 2021
    start = pd.Timestamp(f'{dummy_year}-06-01')
    end = pd.Timestamp(f'{dummy_year}-08-31')

    period_data = {
        'month-day': [],
        'weekly_mean_bloom': [],
        'weekly_std_bloom': [],
    }

    for date in pd.date_range(start=start, end=end, freq='D'):
        print(date)
        values = []
        for stat_date, item in stat.items():
            if stat_date.month == date.month and stat_date.day == date.day:
                values.append(item['weekly_bloom_area'])
        period_data['month-day'].append(date.strftime('%m-%d'))
        period_data['weekly_mean_bloom'].append(round(np.nanmean(values), 1))
        period_data['weekly_std_bloom'].append(round(np.nanstd(values), 1))

    out_file_path = os.path.join(s.setting.export_directory, 'date_weekly_bloom_means.xlsx')

    pd.DataFrame(period_data).to_excel(
        out_file_path,
        sheet_name='data',
        index=False
    )
