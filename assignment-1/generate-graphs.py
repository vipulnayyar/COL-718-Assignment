
import pandas 
import csv
from matplotlib import pyplot

x_axis_cpu_types = ["TIMING", "MINOR", "O3", "ATOMIC"]

x_axis_cpu_freq_types = ["600MHz", "800MHz", "1GHz", "1.2GHz", "1.4GHz", "1.6GHz", "1.8GHz", "2GHz", "2.2GHz", "2.4GHz", "2.6GHz", "2.8GHz", "3GHz", "3.2GHz", "3.3GHz"]

x_axis_memory_model_types = ["SINGLE_CHANNEL_DDR3_1600", "SINGLE_CHANNEL_DDR3_2133", "SINGLE_CHANNEL_LPDDR3_1600", "SINGLE_CHANNEL_DDR4_2400", "SINGLE_CHANNEL_DIMM_DDR5_4400", "SINGLE_CHANNEL_DIMM_DDR5_6400", "SINGLE_CHANNEL_DIMM_DDR5_8400", "DUAL_CHANNEL_DDR3_1600", "DUAL_CHANNEL_DDR3_2133", "DUAL_CHANNEL_LPDDR3_1600", "DUAL_CHANNEL_DDR4_2400" ]

y_axis_freq_wise_metric = {}

DATA = []

def fill_data(results_dir):
    with open(results_dir+"/combined_results.csv", 'r') as csv_file:
        entries = csv.DictReader(csv_file,delimiter=',')

        for entry in entries:
            DATA.append(entry)

def generate_graph_cputypes_vs_perf(metric):
    for entry in DATA:
        if entry['MEMORYMODEL'] != "SINGLE_CHANNEL_DDR3_1600":
            continue


        if entry['CPUFREQUENCY'] not in y_axis_freq_wise_metric:
            y_axis_freq_wise_metric[entry['CPUFREQUENCY']] = [0] * len(x_axis_cpu_types)

        if metric == 'SIMSECONDS':
            y_axis_freq_wise_metric[entry['CPUFREQUENCY']][x_axis_cpu_types.index(entry['CPUTYPE'])] = float(entry[metric]) * 1000
        elif metric == 'CPI':
            y_axis_freq_wise_metric[entry['CPUFREQUENCY']][x_axis_cpu_types.index(entry['CPUTYPE'])] = float(entry[metric])

    print(x_axis_cpu_types)
    print(y_axis_freq_wise_metric)

    for freq, execution_time_entries  in y_axis_freq_wise_metric.items():
        pyplot.plot(x_axis_cpu_types, execution_time_entries, marker = 'o', label=freq)

    pyplot.xlabel('CPU Types')

    if metric == 'SIMSECONDS':
        pyplot.ylabel('Execution Time(ms)')
    elif metric == 'CPI':
        pyplot.ylabel('CPI')
        
    pyplot.title('CPUTypes vs Execution Time for different frequencies(SINGLE_CHANNEL_DDR3_1600)')
    pyplot.grid()
    pyplot.legend()

    pyplot.savefig("cputypes_vs_perf_"+metric+".png")
    #pyplot.show()   

        

fill_data("benchmark_results")
generate_graph_cputypes_vs_perf('SIMSECONDS')
generate_graph_cputypes_vs_perf('CPI')
