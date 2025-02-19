#!/usr/bin/env python

import shutil
import os
import json
import numpy as np
import pandas as pd
from gryffin import Gryffin
from rich.console import Console
from rich.table import Table
from known_constraints import known_constraints
import random

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
        row_str = [f'{i + 1:d}'] + [f'{x:f}' for x in row]
        table.add_row(*row_str)

    console.print(table)

#===============================================================================

# OPTIMIZATION SETTINGS
OBS_FILE = "data.csv"
CONFIG_FILE = "config.json"

# load past experiments
infile_extension = OBS_FILE.split('.')[-1]  # get extension
df_in = load_tabular_data(OBS_FILE, infile_extension)

config = json.load(open(CONFIG_FILE, 'r'))

# check we have all right params/objs in the csv file
obj_names = [obj['name'] for obj in config["objectives"]]  # N.B. order matters
param_names = [param['name'] for param in config["parameters"]]  # N.B. order matters

# drop rows with NaN values in the parameters
df_in = df_in.dropna(subset=param_names)

# show past experiments
print()
print_df_as_rich_table(df_in, title='Past Experiments')

# init gryffin
gryffin = Gryffin(config_file=CONFIG_FILE, known_constraints=known_constraints)


#==============================START=OPTIMIZATION===============================

if len(df_in) == 0:
    observations = []
else:
    # build observation list for Gryffin
    observations = df_to_observations(df_in)



sampling_strategies = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]


samples = gryffin.recommend(observations, sampling_strategies = sampling_strategies)
#samples = gryffin.recommend(observations)

# create df_samples
df_samples = pd.DataFrame(columns=df_in.columns)

for param_name in param_names:
    param_values = [sample[param_name] for sample in samples]
    df_samples.loc[:, param_name] = param_values

# show proposed experiments
print_df_as_rich_table(df_samples, title='Proposed Experiments')
print()

# append df_samples to df_in
df_out = df_in.append(df_samples, ignore_index=True, sort=False)

# make backup of result file
bkp_file = f"backup_{OBS_FILE}"
if os.path.isfile(bkp_file):
    os.remove(bkp_file)
shutil.copy(OBS_FILE, bkp_file)

fin_name = f"G4_{OBS_FILE}"
df_out.to_csv(fin_name, index=False)
