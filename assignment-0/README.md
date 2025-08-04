# COL-718-Assignment

## Build
$ make build

OR 

$ g++ fp_simulator.cpp -o fp_simulator

## Run
$ ./fp_simulator <input_trace> <output_csv>


## Assumptions
* This is an in-order pipeline, hence only RAW data hazards are being handled
* The following instructions are supported with their associated latencies as per the provided Assignment instructions


Instruction with Latency (cycles)

FADD.S 3

FADD.D 5

FSUB.S 3

FSUB.D 5

FMUL.S 4

FMUL.D 6

FDIV.S 10

FDIV.D 16

FMOV.S 1

FMOV.D 1
