#!/bin/bash

GEM5PATH="/Users/vipul/dev/gem5/build/ALL/gem5.opt"
CONFIGPATH="/Users/vipul/dev/COL-718-Assignment/assignment-1/config.py"
BINARYPATH="/Users/vipul/dev/COL-718-Assignment/assignment-1/matrix_multiplication-x86-binary"
BASEDIR=`pwd`
BENCHMARKDIR=${BASEDIR}/benchmark_results

ISATYPES=("X86")
#CPUTYPES=("ATOMIC" "TIMING" "MINOR" "O3" "KVM" )
CPUTYPES=("ATOMIC" "TIMING" "MINOR" "O3" )
CPUFREQUENCIES=("600MHz" "800MHz" "1GHz" "1.2GHz" "1.4GHz" "1.6GHz" "1.8GHz" "2GHz" "2.2GHz" "2.4GHz" "2.6GHz" "2.8GHz" "3GHz" "3.2GHz" "3.3GHz")
MEMORYMODELS=("SINGLE_CHANNEL_DDR3_1600" "SINGLE_CHANNEL_DDR3_2133" "SINGLE_CHANNEL_LPDDR3_1600" "SINGLE_CHANNEL_DDR4_2400" "SINGLE_CHANNEL_DIMM_DDR5_4400" "SINGLE_CHANNEL_DIMM_DDR5_6400" "SINGLE_CHANNEL_DIMM_DDR5_8400" "DUAL_CHANNEL_DDR3_1600" "DUAL_CHANNEL_DDR3_2133" "DUAL_CHANNEL_LPDDR3_1600" "DUAL_CHANNEL_DDR4_2400" )

mkdir -p ${BENCHMARKDIR}
rm -rf ${BENCHMARKDIR}/*
cd ${BENCHMARKDIR}

count=0


for isa in "${ISATYPES[@]}"; do
    for cpu in "${CPUTYPES[@]}"; do
        for cpufreq in "${CPUFREQUENCIES[@]}"; do
            for memory in "${MEMORYMODELS[@]}"; do
               
                echo "Processing ISA $isa"
                echo "Processing CPU TYPE $cpu"
                echo "Processing CPU FREQUENCY $cpufreq"
                echo "Processing MEMORY MODEL $memory"

                ((count++))

                TESTDIR="test_${count}_${isa}_${cpu}_${cpufreq}_${memory}"
                mkdir -p ${TESTDIR}

                rm -f ${TESTDIR}/conf.env

                echo "export COUNT=${count}" >> ${TESTDIR}/conf.env
                echo "export ISA=${isa}" >> ${TESTDIR}/conf.env
                echo "export CPU=${cpu}" >> ${TESTDIR}/conf.env
                echo "export CPUFREQ=${cpufreq}" >> ${TESTDIR}/conf.env
                echo "export MEMORY=${memory}" >> ${TESTDIR}/conf.env
                

                $GEM5PATH --outdir=${TESTDIR} $CONFIGPATH --isa $isa --binary $BINARYPATH --cputype $cpu --cpufrequency $cpufreq --memorymodel $memory &


                
                #break
            done

            wait

            #break
        done

        #break
    done

    #break
done
