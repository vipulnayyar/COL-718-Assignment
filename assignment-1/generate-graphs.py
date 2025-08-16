
import pandas 
import csv
from matplotlib import pyplot

x_axis_cpu_types = ["ATOMIC", "TIMING", "MINOR", "O3"]

x_axis_cpu_freq_types = ["600MHz", "800MHz", "1GHz", "1.2GHz", "1.4GHz", "1.6GHz", "1.8GHz", "2GHz", "2.2GHz", "2.4GHz", "2.6GHz", "2.8GHz", "3GHz", "3.2GHz", "3.3GHz"]

x_axis_memory_model_types = ["SINGLE_CHANNEL_DDR3_1600", "SINGLE_CHANNEL_DDR3_2133", "SINGLE_CHANNEL_LPDDR3_1600", "SINGLE_CHANNEL_DDR4_2400", "SINGLE_CHANNEL_DIMM_DDR5_4400", "SINGLE_CHANNEL_DIMM_DDR5_6400", "SINGLE_CHANNEL_DIMM_DDR5_8400", "DUAL_CHANNEL_DDR3_1600", "DUAL_CHANNEL_DDR3_2133", "DUAL_CHANNEL_LPDDR3_1600", "DUAL_CHANNEL_DDR4_2400" ]


DATA = []

RESULTS_DIR = "benchmark_results"

def fill_data(results_dir):
    with open(results_dir+"/combined_results.csv", 'r') as csv_file:
        entries = csv.DictReader(csv_file,delimiter=',')

        for entry in entries:
            DATA.append(entry)

###########################
def generate_graph_cputypes_vs_perf_fixed_memory_diff_freq(metric):

    pyplot.figure(constrained_layout=True)
    y_axis_freq_wise_metric = {}

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

    for freq, metric_entries  in y_axis_freq_wise_metric.items():
        pyplot.plot(x_axis_cpu_types, metric_entries, marker = 'o', label=freq)

    pyplot.xlabel('CPU Types')

    if metric == 'SIMSECONDS':
        pyplot.ylabel('Execution Time(ms)')
    elif metric == 'CPI':
        pyplot.ylabel('CPI')
        
    pyplot.title(' CPUTypes vs '+metric+' for different frequencies(SINGLE_CHANNEL_DDR3_1600)')
    pyplot.grid()
    pyplot.legend(loc="center left", bbox_to_anchor=(1,0.5))
    pyplot.tight_layout()

    pyplot.savefig(RESULTS_DIR+"/plots/cputypes_vs_"+metric+"_fixed_memory_model_diff_freq.png")

def generate_graph_cputypes_vs_perf_fixed_freq_diff_memory(metric):

    pyplot.figure(constrained_layout=True)
    y_axis_memory_wise_metric = {}

    for entry in DATA:
        if entry['CPUFREQUENCY'] != "3.3GHz":
            continue


        if entry['MEMORYMODEL'] not in y_axis_memory_wise_metric:
            y_axis_memory_wise_metric[entry['MEMORYMODEL']] = [0] * len(x_axis_cpu_types)

        if metric == 'SIMSECONDS':
            y_axis_memory_wise_metric[entry['MEMORYMODEL']][x_axis_cpu_types.index(entry['CPUTYPE'])] = float(entry[metric]) * 1000
        elif metric == 'CPI':
            y_axis_memory_wise_metric[entry['MEMORYMODEL']][x_axis_cpu_types.index(entry['CPUTYPE'])] = float(entry[metric])

    print(x_axis_cpu_types)
    print(y_axis_memory_wise_metric)

    for memory, metric_entries  in y_axis_memory_wise_metric.items():
        pyplot.plot(x_axis_cpu_types, metric_entries, marker = 'o', label=memory)

    pyplot.xlabel('CPU Types')

    if metric == 'SIMSECONDS':
        pyplot.ylabel('Execution Time(ms)')
    elif metric == 'CPI':
        pyplot.ylabel('CPI')
        
    pyplot.title('  CPUTypes vs '+metric+' for different Memory Models(3.3GHz)')
    pyplot.grid()
    pyplot.legend(loc="center left", bbox_to_anchor=(1,0.5))
    pyplot.tight_layout()

    pyplot.savefig(RESULTS_DIR+"/plots/cputypes_vs_"+metric+"_fixed_freq_diff_memory_model.png")

###########################

def generate_graph_freq_vs_perf_fixed_memory_diff_cpu(metric):

    pyplot.figure(constrained_layout=True)
    y_axis_cpu_wise_metric = {}

    for entry in DATA:
        if entry['MEMORYMODEL'] != "SINGLE_CHANNEL_DDR3_1600":
            continue


        if entry['CPUTYPE'] not in y_axis_cpu_wise_metric:
            y_axis_cpu_wise_metric[entry['CPUTYPE']] = [0] * len(x_axis_cpu_freq_types)

        if metric == 'SIMSECONDS':
            y_axis_cpu_wise_metric[entry['CPUTYPE']][x_axis_cpu_freq_types.index(entry['CPUFREQUENCY'])] = float(entry[metric]) * 1000
        elif metric == 'CPI':
            y_axis_cpu_wise_metric[entry['CPUTYPE']][x_axis_cpu_freq_types.index(entry['CPUFREQUENCY'])] = float(entry[metric])

    print(x_axis_cpu_freq_types)
    print(y_axis_cpu_wise_metric)

    for cpu, metric_entries  in y_axis_cpu_wise_metric.items():
        pyplot.plot(x_axis_cpu_freq_types, metric_entries, marker = 'o', label=cpu)

    pyplot.xlabel('CPU Types')

    if metric == 'SIMSECONDS':
        pyplot.ylabel('Execution Time(ms)')
    elif metric == 'CPI':
        pyplot.ylabel('CPI')
        
    pyplot.title(' CPU Frequency vs '+metric+' for different CPU Types(SINGLE_CHANNEL_DDR3_1600)')
    pyplot.grid()
    pyplot.legend(loc="center left", bbox_to_anchor=(1,0.5))
    pyplot.xticks(rotation=45)
    pyplot.tight_layout()

    pyplot.savefig(RESULTS_DIR+"/plots/freq_vs_"+metric+"_fixed_memory_diff_cpu.png")


def generate_graph_freq_vs_perf_fixed_cpu_diff_memory(metric):

    pyplot.figure(constrained_layout=True)
    y_axis_memory_wise_metric = {}

    for entry in DATA:
        if entry['CPUTYPE'] != "TIMING":
            continue


        if entry['MEMORYMODEL'] not in y_axis_memory_wise_metric:
            y_axis_memory_wise_metric[entry['MEMORYMODEL']] = [0] * len(x_axis_cpu_freq_types)

        if metric == 'SIMSECONDS':
            y_axis_memory_wise_metric[entry['MEMORYMODEL']][x_axis_cpu_freq_types.index(entry['CPUFREQUENCY'])] = float(entry[metric]) * 1000
        elif metric == 'CPI':
            y_axis_memory_wise_metric[entry['MEMORYMODEL']][x_axis_cpu_freq_types.index(entry['CPUFREQUENCY'])] = float(entry[metric])

    print(x_axis_cpu_freq_types)
    print(y_axis_memory_wise_metric)

    for cpu, metric_entries  in y_axis_memory_wise_metric.items():
        pyplot.plot(x_axis_cpu_freq_types, metric_entries, marker = 'o', label=cpu)

    pyplot.xlabel('CPU Types')

    if metric == 'SIMSECONDS':
        pyplot.ylabel('Execution Time(ms)')
    elif metric == 'CPI':
        pyplot.ylabel('CPI')
        
    pyplot.title(' CPU Frequency vs '+metric+' for different Memory Model(TIMING CPU)')
    pyplot.grid()
    pyplot.legend(loc="center left", bbox_to_anchor=(1,0.5))
    pyplot.xticks(rotation=45)
    pyplot.tight_layout()

    pyplot.savefig(RESULTS_DIR+"/plots/freq_vs_"+metric+"_fixed_cpu_diff_memory.png")


##########################

def generate_graph_memory_vs_perf_fixed_freq_diff_cpu(metric):

    pyplot.figure(constrained_layout=True)
    y_axis_cpu_wise_metric = {}

    for entry in DATA:
        if entry['CPUFREQUENCY'] != "3.3GHz":
            continue


        if entry['CPUTYPE'] not in y_axis_cpu_wise_metric:
            y_axis_cpu_wise_metric[entry['CPUTYPE']] = [0] * len(x_axis_memory_model_types)

        if metric == 'SIMSECONDS':
            y_axis_cpu_wise_metric[entry['CPUTYPE']][x_axis_memory_model_types.index(entry['MEMORYMODEL'])] = float(entry[metric]) * 1000
        elif metric == 'CPI':
            y_axis_cpu_wise_metric[entry['CPUTYPE']][x_axis_memory_model_types.index(entry['MEMORYMODEL'])] = float(entry[metric])

    print(x_axis_memory_model_types)
    print(y_axis_cpu_wise_metric)

    for memory, metric_entries  in y_axis_cpu_wise_metric.items():
        pyplot.plot(x_axis_memory_model_types, metric_entries, marker = 'o', label=memory)

    pyplot.xlabel('Memory Models')

    if metric == 'SIMSECONDS':
        pyplot.ylabel('Execution Time(ms)')
    elif metric == 'CPI':
        pyplot.ylabel('CPI')
        
    pyplot.title(' Memory Models vs '+metric+' for different CPU Types(3.3GHz)')
    pyplot.grid()
    pyplot.legend(loc="center left", bbox_to_anchor=(1,0.5))
    pyplot.xticks(rotation=45)
    pyplot.tight_layout()

    pyplot.savefig(RESULTS_DIR+"/plots/memory_vs_"+metric+"_fixed_freq_diff_cpu.png")

def generate_graph_memory_vs_perf_fixed_cpu_diff_freq(metric):

    pyplot.figure(constrained_layout=True)
    y_axis_freq_wise_metric = {}

    for entry in DATA:
        if entry['CPUTYPE'] != "TIMING":
            continue


        if entry['CPUFREQUENCY'] not in y_axis_freq_wise_metric:
            y_axis_freq_wise_metric[entry['CPUFREQUENCY']] = [0] * len(x_axis_memory_model_types)

        if metric == 'SIMSECONDS':
            y_axis_freq_wise_metric[entry['CPUFREQUENCY']][x_axis_memory_model_types.index(entry['MEMORYMODEL'])] = float(entry[metric]) * 1000
        elif metric == 'CPI':
            y_axis_freq_wise_metric[entry['CPUFREQUENCY']][x_axis_memory_model_types.index(entry['MEMORYMODEL'])] = float(entry[metric])

    print(x_axis_memory_model_types)
    print(y_axis_freq_wise_metric)

    for freq, metric_entries  in y_axis_freq_wise_metric.items():
        pyplot.plot(x_axis_memory_model_types, metric_entries, marker = 'o', label=freq)

    pyplot.xlabel('Memory Models')

    if metric == 'SIMSECONDS':
        pyplot.ylabel('Execution Time(ms)')
    elif metric == 'CPI':
        pyplot.ylabel('CPI')
        
    pyplot.title(' Memory Models vs '+metric+' for different CPU Types(3.3GHz)')
    pyplot.grid()
    pyplot.legend(loc="center left", bbox_to_anchor=(1,0.5))
    pyplot.xticks(rotation=45)
    pyplot.tight_layout()

    pyplot.savefig(RESULTS_DIR+"/plots/memory_vs_"+metric+"_fixed_cpu_diff_freq.png")


##########################
fill_data(RESULTS_DIR)

##########################

generate_graph_cputypes_vs_perf_fixed_memory_diff_freq('SIMSECONDS')
generate_graph_cputypes_vs_perf_fixed_memory_diff_freq('CPI')

generate_graph_cputypes_vs_perf_fixed_freq_diff_memory('SIMSECONDS')
generate_graph_cputypes_vs_perf_fixed_freq_diff_memory('CPI')

#########################


generate_graph_freq_vs_perf_fixed_memory_diff_cpu('SIMSECONDS')
generate_graph_freq_vs_perf_fixed_memory_diff_cpu('CPI')

generate_graph_freq_vs_perf_fixed_cpu_diff_memory('SIMSECONDS')
generate_graph_freq_vs_perf_fixed_cpu_diff_memory('CPI')

#########################

generate_graph_memory_vs_perf_fixed_freq_diff_cpu('SIMSECONDS')
generate_graph_memory_vs_perf_fixed_freq_diff_cpu('CPI')

generate_graph_memory_vs_perf_fixed_cpu_diff_freq('SIMSECONDS')
generate_graph_memory_vs_perf_fixed_cpu_diff_freq('CPI')





