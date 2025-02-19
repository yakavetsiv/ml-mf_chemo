# Gryffin Optimization Framework

This repository contains code for running optimization experiments using the Gryffin optimization framework. The code supports both sequential and concurrent optimization strategies for drug combination studies.

## Package Structure

```
.
├── FAC/                    # 5-FU + DOX + CPA Drug Combination experiments using MCF-7 spheroids
│   ├── concurrent/        # Concurrent optimization experiments
│   │   ├── data/
│   │   │   └── data_FAC_con.csv
│   │   ├── G0/
│   │   │   ├── config.json
│   │   │   └── run_gryffin.py
│   │   ├── G1-G2/
│   │   │   ├── config.json
│   │   │   ├── known_constraints.py
│   │   │   ├── util.py
│   │   │   └── run_gryffin.py
│   │   └── G3-G4/
│   │       ├── config.json
│   │       ├── known_constraints.py
│   │       ├── util.py
│   │       └── run_gryffin.py
│   └── sequential/        # Sequential optimization experiments
│       ├── data/
│       │   └── data_FAC_seq.csv
│       ├── GS0-GS1/
│       │   ├── known_constraints.py
│       │   └── run_gryffin.py
│       ├── GS2/
│       │   ├── known_constraints.py
│       │   └── run_gryffin.py
│       └── GS3/
│           ├── known_constraints.py
│           └── run_gryffin.py
│
├── OLA-IBET/              # OLA-IBET Drug Combination experiments using breast cancer PDOs
│   ├── concurrent/        # Concurrent optimization experiments
│   │   ├── data/
│   │   │   └── data_OLA-IBET_con.csv
│   │   ├── G3/
│   │   │   ├── data.csv
│   │   │   └── run_gryffin.py
│   │   └── G4/
│   │       ├── data.csv
│   │       └── run_gryffin.py
│   └── sequential/        # Sequential optimization experiments
│       ├── data/
│       │   └── data_OLA-IBET_seq.csv
│       ├── GS0/
│       │   └── run_gryffin.py
│       └── GS1-GS2/
│           ├── known_constraints.py
│           └── run_gryffin.py
│
├── requirements.txt       # Project dependencies
├── README.md             # Project documentation
└── LICENSE               # License information
```

## Overview

The framework includes:
- Sequential optimization 
- Concurrent optimization 
- Support for both categorical/discrete and continuous parameters
- Multiple optimization objectives
- Rich console output for experiment visualization

## Detailed Installation Guide for Linux

### 1. Create directories
```bash
mkdir anaconda
mkdir gryffin
```

### 2. Install Anaconda
```bash
wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
bash Anaconda3-2020.11-Linux-x86_64.sh
export PATH="/home/ekg/anaconda3/bin:$PATH"
```

### 3. Create and activate Gryffin environment
```bash
conda create -n gryffin python=3.7
source activate gryffin
```

### 4. Install Dependencies
There are two ways to install the required packages:

#### Option 1: Using requirements.txt (Recommended)
```bash
pip install -r requirements.txt
```
This will install all necessary packages with specific versions:
- Core dependencies (numpy, pandas, tensorflow)
- Gryffin and its dependencies
- Data processing libraries
- Console output utilities
- Build requirements

#### Option 2: Manual Installation
```bash
conda install numpy scipy sqlalchemy cython pandas
pip install tensorflow==2.3
pip install tensorflow-probability==0.11
```

### 5. Install Gryffin
```bash
cd gryffin/
git clone https://github.com/aspuru-guzik-group/gryffin.git
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install gcc -y
cd gryffin/
pip install .
git checkout master
```

### 6. Setup working directory
```bash
cd ..
mkdir example_gryffin
cd example_gryffin
chmod +x run_gryffin.py
```

### WSL Usage
If using Windows Subsystem for Linux (WSL):
```bash
source activate gryffin
cd /mnt/c/Users/username/path/to/gryffin
cd example_gryffin
gryffin -f data.csv -c config.json -n 5
```

## Dependencies Details

The project requires several Python packages that are specified in `requirements.txt`:

```text
# Core dependencies
numpy>=1.19.2        # For numerical computations
pandas>=1.1.3        # For data manipulation
tensorflow==2.3.0    # ML backend
tensorflow-probability==0.11.0

# Gryffin specific
gryffin @ git+https://github.com/aspuru-guzik-group/gryffin.git@master

# Data processing
scipy>=1.5.2         # Scientific computing
sqlalchemy>=1.3.20   # Database operations
cython>=0.29.21      # Performance optimization
openpyxl>=3.0.5      # Excel file support

# Console output
rich>=10.0.0         # Enhanced terminal output

# Build requirements
setuptools>=50.3.1
wheel>=0.35.1
```

To update dependencies in the future:
```bash
pip install --upgrade -r requirements.txt
```

## Features

- Load and process experimental data from CSV/Excel files
- Support for known constraints
- Data normalization and inverse transformation
- Backup functionality for experimental results
- Rich console output using the `rich` library
- Configurable sampling strategies
- Support for multiple optimization objectives

## Configuration

The optimization can be configured through the `CONFIG` dictionary in the script:
- General settings (batches, CPUs, random seed, etc.)
- Parameter definitions (continuous, discrete, categorical)
- Optimization objectives and tolerances

## Output

The script generates:
- Rich console output showing past and proposed experiments
- CSV files with optimization results
- Optional backup files of the results

## Usage

To run an optimization:

1. Prepare your data file (CSV format)
2. Configure the optimization parameters in the script
3. Run the script:
```bash
python run_gryffin.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.