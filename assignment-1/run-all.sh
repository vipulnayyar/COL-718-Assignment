#!/bin/bash

bash bench.sh
bash collect-csv-from-benchmarks.sh
python3 generate-graphs.py
