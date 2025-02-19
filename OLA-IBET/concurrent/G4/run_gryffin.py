#!/usr/bin/env python

import os
import json
import shutil
import numpy as np
import pandas as pd
from gryffin import Gryffin
from rich.console import Console
from rich.table import Table
from known_constraints import known_constraints
from utils import norm_data_inverse

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
OBS_FILE = "data.csv"

sampling_strategies = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
#sampling_strategies = np.array([i*2/10-1  for i in range(10)]).astype(float)

fit_params = {"drug": ["OLA", "IBET-762"], "fit": [[1, 0.34, 1.53, 123],[0.99, 0.35, 3.42, 468]], "bounds": [[10, 1000], [0.01, 300]], "stock": [5000, 5000], "ctrl":0.879}


CONFIG = {
     "general": {
             "auto_desc_gen": False,
             "batches": 1,
             "num_cpus": 4,
             "boosted":  False,
             "caching": True,
             "backend": "tensorflow",
             "save_database": False,
             "sampling_strategies": 10,
             "random_seed": 100700,
             "feas_approach": "fca",
             "feas_param": 0.2,  # used only if naive is False
             "acquisition_optimizer": "adam",
             "verbosity": 3  # show only warnings and errors and stats
                },

    "parameters": [
          {"name": "conc0", "type": "continuous", "low": 0.0, "high": 1.0, "size": 1},
          {"name": "conc1", "type": "continuous", "low": 0.0, "high": 1.0, "size": 1},
    ],
    "objectives": [{"name": "ci", "goal": "min", "tolerance":-0.15, "absolute": True},
               {"name": "cv_exp", "goal": "min", "tolerance": 0.5, "absolute": True},
    ],
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
gryffin = Gryffin(config_dict=CONFIG, known_constraints=known_constraints)



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
    if param_name in ['t0', 't1']:
        # convert discrete times from gryffin value to real value
        param_values = [sample[param_name] for sample in samples]
    else:
        param_values = [sample[param_name] for sample in samples]
    df_samples.loc[:, param_name] = param_values

# show proposed experiments
print_df_as_rich_table(df_samples, title='Proposed Experiments')
print()

df_samples['gen'] = 4
df_samples['number'] = df_samples.index +1

print(df_samples)

# append df_samples to df_in
df_out = df_in.append(df_samples, ignore_index=True, sort=False)
df_inv = norm_data_inverse(df_out, fit_params['bounds'])
df_out['conc0_inv'] = df_inv['conc0']
df_out['conc1_inv'] = df_inv['conc1']

# make backup of result file
bkp_file = f"backup_{OBS_FILE}"
new_file = f"G4_{OBS_FILE}"
if os.path.isfile(bkp_file):
    os.remove(bkp_file)
#shutil.copy(OBS_FILE, bkp_file)

df_out.to_csv(new_file, index=False)
