
import pandas 
import csv
from matplotlib import pyplot

x_axis_cpu_types = ["ATOMIC", "TIMING", "MINOR", "O3"]

x_axis_cpu_freq_types = ["600MHz", "800MHz", "1GHz", "1.2GHz", "1.4GHz", "1.6GHz", "1.8GHz", "2GHz", "2.2GHz", "2.4GHz", "2.6GHz", "2.8GHz", "3GHz", "3.2GHz", "3.3GHz"]

x_axis_memory_model_types = ["SINGLE_CHANNEL_DDR3_1600", "SINGLE_CHANNEL_DDR3_2133", "SINGLE_CHANNEL_LPDDR3_1600", "SINGLE_CHANNEL_DDR4_2400", "SINGLE_CHANNEL_DIMM_DDR5_4400", "SINGLE_CHANNEL_DIMM_DDR5_6400", "SINGLE_CHANNEL_DIMM_DDR5_8400", "DUAL_CHANNEL_DDR3_1600", "DUAL_CHANNEL_DDR3_2133", "DUAL_CHANNEL_LPDDR3_1600", "DUAL_CHANNEL_DDR4_2400" ]


DATA = []

RESULTS_DIR = "benchmark_results"

figure_count = 1

def fill_data(results_dir):
    with open(results_dir+"/combined_results.csv", 'r') as csv_file:
        entries = csv.DictReader(csv_file,delimiter=',')

        for entry in entries:
            DATA.append(entry)

###########################

def generate_graph_generic(count, x_axis, x_axis_field, perf_metric, variant_field, invariant_field, invariant_value, jitter_value):

    """
    print(x_axis_field)
    print(perf_metric)
    print(variant_field)
    print(invariant_field, invariant_value) """

    global figure_count

    pyplot.figure(constrained_layout=True)
    y_axis = {}

    jitter = 0
    for entry in DATA:
       
        if entry[invariant_field] != invariant_value:
            continue

        #print(entry)

        if entry[variant_field] not in y_axis:
            y_axis[entry[variant_field]] = [0] * len(x_axis)

        if perf_metric == 'SIMSECONDS':
            y_axis[entry[variant_field]][x_axis.index(entry[x_axis_field])] = float(entry[perf_metric]) * 1000
            
            y_axis[entry[variant_field]][x_axis.index(entry[x_axis_field])] += jitter * jitter_value

        elif perf_metric == 'CPI':
            y_axis[entry[variant_field]][x_axis.index(entry[x_axis_field])] = float(entry[perf_metric])

            y_axis[entry[variant_field]][x_axis.index(entry[x_axis_field])] += jitter * jitter_value

        jitter += 1


    print(x_axis)
    print(y_axis)

    
    for freq, metric_entries  in y_axis.items():
        pyplot.plot(x_axis, metric_entries, marker = 'o', label=freq)

    pyplot.xlabel(x_axis_field)
    if x_axis_field == 'CPUFREQUENCY':
        pyplot.xticks(rotation=60)
    elif x_axis_field == 'MEMORYMODEL':
        pyplot.xticks(rotation=80)

    if perf_metric == 'SIMSECONDS':
        pyplot.ylabel('Execution Time(ms)')
    elif perf_metric == 'CPI':
        pyplot.ylabel('CPI')
        
    pyplot.grid()
    pyplot.legend(loc="center left", bbox_to_anchor=(1,0.5))
    
    description = 'Figure '+ str(figure_count) + ': '+x_axis_field +' vs '+perf_metric+' for different frequencies(SINGLE_CHANNEL_DDR3_1600).'

    if jitter_value > 0 :
        description += ' Added jitter(' + str(jitter_value) +') to show overlapping line graphs.'

    figure_count += 1

    pyplot.figtext(0.1, 0.02, description, fontsize=10, ha='left', va='bottom', wrap=True)

    pyplot.tight_layout()

    if x_axis_field == 'MEMORYMODEL':
        pyplot.subplots_adjust(bottom=0.7)
    elif x_axis_field == 'CPUTYPE':
        pyplot.subplots_adjust(bottom=0.2)
    else:
        pyplot.subplots_adjust(bottom=0.3)
    
    pyplot.savefig(RESULTS_DIR+"/plots/"+x_axis_field+"_vs_"+perf_metric+"_fixed_" + invariant_field + "_diff_"+ variant_field +".png")

##########################

fill_data(RESULTS_DIR)

##########################


generate_graph_generic(figure_count, x_axis_cpu_types, 'CPUTYPE', 'SIMSECONDS', 'CPUFREQUENCY', 'MEMORYMODEL', 'SINGLE_CHANNEL_DDR3_1600',0)

generate_graph_generic(figure_count, x_axis_cpu_types, 'CPUTYPE', 'CPI', 'CPUFREQUENCY', 'MEMORYMODEL', 'SINGLE_CHANNEL_DDR3_1600',0.005)


generate_graph_generic(figure_count, x_axis_cpu_types, 'CPUTYPE', 'SIMSECONDS', 'MEMORYMODEL', 'CPUFREQUENCY', '3.3GHz',0.1)



generate_graph_generic(figure_count, x_axis_cpu_types, 'CPUTYPE', 'CPI', 'MEMORYMODEL', 'CPUFREQUENCY', '3.3GHz',0.005)

#########################

generate_graph_generic(figure_count, x_axis_cpu_freq_types, 'CPUFREQUENCY', 'SIMSECONDS', 'CPUTYPE', 'MEMORYMODEL', 'SINGLE_CHANNEL_DDR3_1600',0)

generate_graph_generic(figure_count, x_axis_cpu_freq_types, 'CPUFREQUENCY', 'CPI', 'CPUTYPE', 'MEMORYMODEL', 'SINGLE_CHANNEL_DDR3_1600',0)


generate_graph_generic(figure_count, x_axis_cpu_freq_types, 'CPUFREQUENCY', 'SIMSECONDS', 'MEMORYMODEL', 'CPUTYPE', 'TIMING', 0.5)

generate_graph_generic(figure_count, x_axis_cpu_freq_types, 'CPUFREQUENCY', 'CPI', 'MEMORYMODEL', 'CPUTYPE', 'TIMING', 0)


#########################

generate_graph_generic(figure_count, x_axis_memory_model_types, 'MEMORYMODEL', 'SIMSECONDS', 'CPUTYPE', 'CPUFREQUENCY', '3.3GHz', 0)

generate_graph_generic(figure_count, x_axis_memory_model_types, 'MEMORYMODEL', 'CPI', 'CPUTYPE', 'CPUFREQUENCY', '3.3GHz', 0)


generate_graph_generic(figure_count, x_axis_memory_model_types, 'MEMORYMODEL', 'SIMSECONDS', 'CPUFREQUENCY', 'CPUTYPE', 'TIMING', 0)

generate_graph_generic(figure_count, x_axis_memory_model_types, 'MEMORYMODEL', 'CPI', 'CPUFREQUENCY', 'CPUTYPE', 'TIMING',0)
