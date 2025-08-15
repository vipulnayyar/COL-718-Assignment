#!/bin/bash


RESULTSPATH="${1:-"benchmark_results"}"

echo "Collecting result from ${RESULTSPATH}"

rm -f "${RESULTSPATH}"/combined_results.csv
touch "${RESULTSPATH}"/combined_results.csv

rm -rf "${RESULTSPATH}"/plots

echo "ISA,CPUTYPE,CPUFREQUENCY,MEMORYMODEL,SIMSECONDS,CPI" >> "${RESULTSPATH}"/combined_results.csv

for dir in `ls -tr1 "${RESULTSPATH}"/`; do

    #echo $dir
    if [[ -d "${RESULTSPATH}/${dir}" ]]; then
        echo "Processing dir ${dir}"

        source "${RESULTSPATH}/${dir}/conf.env"
    
        simseconds=`cat ${RESULTSPATH}/${dir}/stats.txt | grep simSeconds | awk '{print $2}'`
        cpi=`cat ${RESULTSPATH}/${dir}/stats.txt | grep board.processor.cores.core.cpi | awk '{print $2}'`

        echo "${ISA},${CPU},${CPUFREQ},${MEMORY},${simseconds},${cpi}" >> "${RESULTSPATH}"/combined_results.csv

    
    fi
done
                
mkdir -p "${RESULTSPATH}"/plots
