#!/usr/bin/env python

import os
import json
import shutil
import numpy as np
import pandas as pd
from gryffin import Gryffin
from rich.console import Console
from rich.table import Table

#==============================UTILS============================================

def load_tabular_data(args, infile_extension):
    # load data
    if infile_extension == 'csv':
        df_in = pd.read_csv(args)
    elif infile_extension in ['xls', 'xlsx']:
        df_in = pd.read_excel(args)

    # rm rows if NaN in parameters. NaN in objective is allowed as infeasible experiment.

    return df_in

def df_to_observations(df):
    observations = []
    for index, row in df.iterrows():
        d = {}
        for col in df.columns:
            # change discrete time observations from true values to gryffin values
            if col in ['t0', 't1']:
                d[col] = row[col]
            else:
                d[col] = row[col]
        observations.append(d)
    return observations


def print_df_as_rich_table(df, title):
    console = Console()

    table = Table(show_header=True, header_style="bold red", title=title)
    table.add_column("N")
    for col in df.columns:
        table.add_column(col)

    np_data = df.to_numpy()
    for i, row in enumerate(np_data):
        row_str = [f'{i + 1:d}'] + [f'{x}' for x in row]
        table.add_row(*row_str)

    console.print(table)


#===============================================================================

# OPTIMIZATION SETTINGS
OBS_FILE = "data.csv" #empty *.csv file

sampling_strategies = np.array([i*2/8-1  for i in range(9)]).astype(float)

CONFIG = {
     "general": {
             "auto_desc_gen": False,
             "batches": 1,
             "num_cpus": 4,
             "boosted":  False,
             "caching": True,
             "backend": "tensorflow",
             "save_database": False,
             "sampling_strategies": 9,
             "random_seed": 100700,
             "feas_approach": "fca",
             "feas_param": 0.2,  # used only if naive is False
             "acquisition_optimizer": "adam",
             "verbosity": 3  # show only warnings and errors and stats
                },

    "parameters": [
          {"name": "seq", "type": "categorical", "category_details": {"a": None, "b": None}},
          {"name": "t0", "type": "discrete", "low": 1, "high": 11},
    ],
    "objectives": [
          {"name": "cv", "goal": "min", "tolerance":0.4, "absolute": True}
    ]
}


#===============================================================================

# load past experiments
infile_extension = OBS_FILE.split('.')[-1]  # get extension
df_in = load_tabular_data(OBS_FILE, infile_extension)

# config = json.load(open(CONFIG_FILE, 'r'))

# check we have all right params/objs in the csv file
obj_names = [obj['name'] for obj in CONFIG["objectives"]]  # N.B. order matters
param_names = [param['name'] for param in CONFIG["parameters"]]  # N.B. order matters

# drop rows with NaN values in the parameters
df_in = df_in.dropna(subset=param_names)

# show past experiments
print()
print_df_as_rich_table(df_in, title='Past Experiments')

# init gryffin
# TODO: switch this back to include known constraints
gryffin = Gryffin(config_dict=CONFIG)



#==============================START=OPTIMIZATION===============================

if len(df_in) == 0:
    observations = []
else:
    # build observation list for Gryffin
    observations = df_to_observations(df_in)

#RECOMMEND SAMPLES
#samples = []
#for sampling_strategy in sampling_strategies:
#    samples.append(
#           gryffin.recommend(observations, sampling_strategies=[sampling_strategy])[0]
#        )
        
samples = gryffin.recommend(observations, sampling_strategies = sampling_strategies)
#samples = gryffin.recommend(observations)

#print('SAMPLES : ', samples)

# create df_samples
df_samples = pd.DataFrame(columns=df_in.columns)



for param_name in param_names:
    if param_name in ['t0']:
        # convert discrete times from gryffin value to real value
        param_values = [sample[param_name] for sample in samples]
    else:
        param_values = [sample[param_name] for sample in samples]
    df_samples.loc[:, param_name] = param_values

# show proposed experiments
print_df_as_rich_table(df_samples, title='Proposed Experiments')
print()

df_samples['gen'] = 0
df_samples['number'] = df_samples.index +1
df_samples['t1'] = 12-df_samples['t0']
print(df_samples)

# append df_samples to df_in
df_out = df_in.append(df_samples, ignore_index=True, sort=False)


# make backup of result file
bkp_file = f"backup_{OBS_FILE}"
new_file = f"GS0_{OBS_FILE}"
if os.path.isfile(bkp_file):
    os.remove(bkp_file)
#shutil.copy(OBS_FILE, bkp_file)

df_out.to_csv(new_file, index=False)
