
# Assignment 1

## Setup

Activate venv environment
```
$ source venv/bin/activate
```

Add paths in bench.sh
```
$ vim bench.sh

GEM5PATH="/Users/vipul/dev/gem5/build/ALL/gem5.opt"
CONFIGPATH="/Users/vipul/dev/COL-718-Assignment/assignment-1/config.py"
BINARYPATH="/Users/vipul/dev/COL-718-Assignment/assignment-1/matrix_multiplication-x86-binary"
```

Run bench.sh to start simulations
```
$ bash bench.sh
```

Collect simulation stats in combined csv file
```
$ bash collect-csv-from-benchmarks.sh
```
Combined results will be added to ./benchmark_results/combined_results.csv file

Generate graphs
```
$ python3 generate-graphs.py
```

Graphs will be generated in ./benchmark_results/plots directory.
