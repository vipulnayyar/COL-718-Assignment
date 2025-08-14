

RESULTSPATH="${1:-"benchmark_results"}"

echo "${RESULTSPATH}"

rm -f "${RESULTSPATH}"/combined_results.csv
touch "${RESULTSPATH}"/combined_results.csv
echo "Count,ISA,CPUTYPE,CPUFREQUENCY,MEMORYMODEL,SIMSECONDS,CPI" >> "${RESULTSPATH}"/combined_results.csv

for dir in `ls -tr1 "${RESULTSPATH}"/`; do

    if [[ -d "${RESULTSPATH}/${dir}" ]]; then
        echo "Processing dir ${dir}"

        source "${RESULTSPATH}/${dir}/conf.env"
    
        simseconds=`cat ${RESULTSPATH}/${dir}/m5out/stats.txt | grep simSeconds | awk '{print $2}'`
        cpi=`cat ${RESULTSPATH}/${dir}/m5out/stats.txt | grep board.processor.cores.core.cpi | awk '{print $2}'`

        echo "${COUNT},${ISA},${CPU},${CPUFREQ},${MEMORY},${simseconds},${cpi}" >> "${RESULTSPATH}"/combined_results.csv

    
    fi
done
                